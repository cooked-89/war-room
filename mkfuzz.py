# -*- coding: utf-8 -*-
"""A soak test: random operations against the real app, invariants checked after each."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

src = open("draft-room.html", encoding="utf-8").read()
guard = ('<script>window.__errs=[];window.addEventListener("error",function(e){'
         'window.__errs.push(e.message+" @"+e.lineno+":"+e.colno)});'
         'window.addEventListener("unhandledrejection",function(e){'
         'window.__errs.push("REJECT "+e.reason)});</script>\n')

FUZZ = r'''
<script>
setTimeout(function(){
  var out = [], failures = [];
  var LEAGUES_K = Object.keys(LEAGUES);

  // deterministic RNG so a failure can be reproduced from its seed
  var seed = 20260819;
  function rnd(){ seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
  function pick(a){ return a[Math.floor(rnd() * a.length) % a.length]; }
  function iRnd(n){ return Math.floor(rnd() * n); }

  function scanRendered(errs){
    if(window.__forceScanFail) errs.push("FORCED");
    /* numbers that leak as NaN or undefined are the classic rendering bug, and they
       are invisible to logic-only assertions */
    ["boardBody","recs","teamOut","weekOut","queueOut","cowOut","depthOut","intelBody","sosOut","diaryOut"]
      .forEach(function(id){
        var el = document.getElementById(id);
        if(!el) return;
        var t = el.textContent || "";
        if(t.indexOf("NaN") >= 0) errs.push("NaN rendered in #"+id);
        if(t.indexOf("undefined") >= 0) errs.push("undefined rendered in #"+id);
        if(/\[object Object\]/.test(t)) errs.push("[object Object] rendered in #"+id);
      });

  }

  /* Things that must be true no matter what the user just did. */
  function invariants(where){
    var errs = [];
    scanRendered(errs);
    var total = totalPicks();
    if(state.picks.length > total)
      errs.push("more picks ("+state.picks.length+") than slots ("+total+")");

    var seen = Object.create(null);
    for(var i=0;i<state.picks.length;i++){
      var pk = state.picks[i];
      if(!byId.has(pk.playerId)){ errs.push("pick "+i+" references an unknown player"); break; }
      if(seen[pk.playerId]){ errs.push("player drafted twice: "+byId.get(pk.playerId).name); break; }
      seen[pk.playerId] = 1;
      if(pk.team < 0 || pk.team >= state.teams){ errs.push("pick "+i+" has team "+pk.team); break; }
      if(teamOnClock(i) !== pk.team){
        errs.push("snake broken at pick "+i+": stored "+pk.team+", clock says "+teamOnClock(i)); break;
      }
    }
    if(state.slot < 1 || state.slot > state.teams)
      errs.push("slot "+state.slot+" outside 1.."+state.teams);
    if(state.rounds < 1) errs.push("rounds "+state.rounds);
    if(PLAYERS.length === 0) errs.push("empty player board");
    var L = LEAGUES[state.league];
    (L.drop||[]).forEach(function(pos){
      if(PLAYERS.some(function(p){ return p.pos===pos; })) errs.push(pos+" not dropped");
    });
    Object.keys(state.byLeague).forEach(function(k){
      var e = state.byLeague[k];
      if(e && e.slot && e.slot > LEAGUES[k].teams) errs.push("stashed slot for "+k+" exceeds team count");
    });

    /* a player must never be both a starter and on the bench */
    if(state.picks.length){
      var bl = bestLineup(rosterOf(myIdx()));
      var st = {};
      bl.slots.forEach(function(f){ if(f.p){ if(st[f.p.id]) errs.push("player starts twice: "+f.p.name); st[f.p.id]=1; } });
      if(bl.points < 0) errs.push("negative lineup points");
      var rsize = rosterOf(myIdx()).length;
      if(bl.slots.filter(function(f){return f.p;}).length > rsize)
        errs.push("lineup uses more players than the roster holds");
    }

    /* projections and value must be numbers or explicitly null - never NaN */
    for(var j=0;j<PLAYERS.length;j++){
      var p = PLAYERS[j];
      if(p.proj !== null && !isFinite(p.proj)){ errs.push("non-finite proj on "+p.name); break; }
      if(p.vorp !== null && !isFinite(p.vorp)){ errs.push("non-finite vorp on "+p.name); break; }
      if(!isFinite(p.adp)){ errs.push("non-finite adp on "+p.name); break; }
    }
    if(errs.length) failures.push(where + " -> " + errs.join("; "));
    return errs.length === 0;
  }

  var ops = [
    ["switch league", function(){ applyLeague(pick(LEAGUES_K)); }],
    ["change slot",   function(){ state.slot = 1 + iRnd(state.teams); }],
    ["toggle sim",    function(){ state.sim = !state.sim; }],
    ["run sim",       function(){ runSim(); }],
    ["draft top rec", function(){ var r = recommend(); if(r.length) makePick(r[0].p.id); }],
    ["draft random",  function(){ var a = available(); if(a.length) makePick(a[iRnd(Math.min(20,a.length))].id); }],
    ["undo",          function(){
        if(!state.picks.length) return;
        if(state.sim){
          var i = state.picks.length-1;
          while(i>=0 && state.picks[i].team !== (state.slot-1)) i--;
          state.picks = state.picks.slice(0, Math.max(i,0));
        } else state.picks.pop();
      }],
    ["reset",         function(){ state.picks = []; delete state.byLeague[state.league]; reseed(); }],
    ["star/avoid",    function(){
        var p = PLAYERS[iRnd(PLAYERS.length)];
        if(rnd() < 0.5){ state.star.has(p.id) ? state.star.delete(p.id) : state.star.add(p.id); }
        else { state.avoid.has(p.id) ? state.avoid.delete(p.id) : state.avoid.add(p.id); }
      }],
    ["import names",  function(){
        var a = available().slice(0, 1 + iRnd(8)).map(function(p){ return p.name; });
        applyNames(a);
      }],
    ["import junk",   function(){ applyNames(["Not A Player", "", "  ", "12345"]); }],
    ["hash sync",     function(){
        var a = available().slice(0, 3).map(function(p){ return p.name; }).join("|");
        location.hash = "#draft=" + state.league + ":" + encodeURIComponent(a);
        importFromHash();
        location.hash = "";
      }],
    ["sort",          function(){ state.sortBy = pick(["adp","vorp","proj"]); }],
    ["live adp",      function(){ state.useLiveAdp = !state.useLiveAdp; applyLeague(state.league); }],
    ["change rounds", function(){ state.rounds = 13 + iRnd(4); }],
    ["trade toggle",  function(){
        var r = rosterOf(myIdx());
        if(r.length){ var p = r[iRnd(r.length)];
          state.tradeOut.has(p.id) ? state.tradeOut.delete(p.id) : state.tradeOut.add(p.id); }
        evaluateTrade();
      }],
    ["render all",    function(){ renderBoard(); renderDraft(); renderTeam(); renderDepth();
                                  renderIntel(); renderCliffs(); renderSOS(); renderDraftDiary(); }],
    ["slot plan",     function(){ if(rnd() < 0.15) slotReport(state.slot, 2); }],
    ["save/load",     function(){ save(); }]
  ];

  /* Prove the detector works before trusting a clean run. invariants() returns
     false when it finds something, so check that directly rather than poking at a
     shared array. Each deliberate fault must be caught. */
  var selfCheck = [];
  (function(){
    state.picks = []; state.byLeague = {}; applyLeague("espn10");
    function probe(name, breakIt){
      var undo = breakIt();
      var lenBefore = failures.length;
      var ok = invariants("selfcheck:" + name);
      failures.length = lenBefore;          // discard the deliberate failure
      undo();
      if(ok) selfCheck.push(name);
    }
    probe("scan wiring", function(){
      window.__forceScanFail = true;
      return function(){ window.__forceScanFail = false; };
    });
    probe("non-finite proj", function(){
      var p = PLAYERS[0], old = p.proj; p.proj = NaN;
      return function(){ p.proj = old; };
    });
    probe("NaN in render", function(){
      var el = document.getElementById("boardBody"), old = el.innerHTML;
      el.innerHTML = "<tr><td>NaN</td></tr>";
      return function(){ el.innerHTML = old; };
    });
    probe("undefined in render", function(){
      var el = document.getElementById("cowOut"), old = el.innerHTML;
      el.innerHTML = "<div>undefined</div>";
      return function(){ el.innerHTML = old; };
    });
    probe("broken snake", function(){
      var old = state.picks;
      state.picks = [{playerId: PLAYERS[0].id, team: 99, overall: 0}];
      return function(){ state.picks = old; };
    });
    probe("duplicate pick", function(){
      var old = state.picks, id = PLAYERS[0].id;
      state.picks = [{playerId:id, team:teamOnClock(0), overall:0},
                     {playerId:id, team:teamOnClock(1), overall:1}];
      return function(){ state.picks = old; };
    });
    state.picks = []; state.byLeague = {}; applyLeague("espn10");
  })();

  var SEEDS = [20260819, 7, 424242, 99991, 31337], PER = 400, opCount = {}, total = 0;
  SEEDS.forEach(function(sd){
    seed = sd;
    state.picks = []; state.byLeague = {}; state.star.clear(); state.avoid.clear();
    applyLeague("espn10");
    for(var step=0; step<PER && failures.length < 12; step++){
      var op = pick(ops);
      opCount[op[0]] = (opCount[op[0]] || 0) + 1;
      total++;
      try{
        op[1]();
      }catch(e){
        failures.push("seed "+sd+" op '" + op[0] + "' threw: " + e.message);
        continue;
      }
      if(!invariants("seed "+sd+" after '" + op[0] + "' (step " + step + ")")) {
        state.picks = []; state.byLeague = {}; applyLeague(state.league);
      }
    }
  });

  out.push("detector self-check: " + (selfCheck.length ? ("MISSED -> " + selfCheck.join(", ")) : "all 5 deliberate faults caught"));
  out.push("operations run: " + total + " across " + SEEDS.length + " seeds");
  out.push("distinct ops: " + Object.keys(opCount).length);
  out.push("runtime errors: " + (window.__errs.length ? window.__errs.slice(0,5).join(" | ") : "none"));
  out.push(failures.length ? ("FAILURES (" + failures.length + "):\n  " + failures.slice(0,12).join("\n  "))
                           : "INVARIANTS HELD across all operations");

  var pre = document.createElement("pre");
  pre.id = "FUZZLOG";
  pre.textContent = out.join("\n");
  document.body.appendChild(pre);
}, 400);
</script>
'''

open("fuzz.html", "w", encoding="utf-8").write(guard + src + FUZZ)
print("fuzz.html built")
