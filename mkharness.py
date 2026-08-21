import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Which file to test. The default is the app source, but the BUILT artifact must also
# be testable: live sync once lived only in build_pwa.py's tail, invisible to this
# harness, and a duplicate implementation was written because of it. Test what ships.
#   python mkharness.py            -> test-harness.html      from draft-room.html
#   python mkharness.py --built    -> test-harness-built.html from pwa/index.html
import sys as _sys
_built = "--built" in _sys.argv
_srcfile = "pwa/index.html" if _built else "draft-room.html"
_outfile = "test-harness-built.html" if _built else "test-harness.html"
src = open(_srcfile, encoding="utf-8").read()
if _built:
    # The built file is a whole document; strip the wrapper so the harness can append
    # to the same page, and neutralise the service worker, which has no business
    # running inside a test.
    src = src.replace('navigator.serviceWorker.register("sw.js")', 'Promise.resolve()')
    for _tag in ("<!doctype html>", "<!DOCTYPE html>"):
        src = src.replace(_tag, "")
    src = src.replace("</body>", "").replace("</html>", "")
    # the harness supplies its own network posture
    src = src.replace("window.LIVE_CAPABLE = true;", "window.LIVE_CAPABLE = false;")
guard = '<script>window.__errs=[];window.addEventListener("error",function(e){window.__errs.push(e.message+" @line "+e.lineno+":"+e.colno)});</script>\n'

MFL_FIXTURE = '{"draftResults": {"draftUnit": {"draftPick": [{"round": "01", "pick": "01", "franchise": "0012", "player": ""}, {"round": "01", "pick": "02", "franchise": "0008", "player": ""}, {"round": "01", "pick": "03", "franchise": "0006", "player": ""}, {"round": "01", "pick": "04", "franchise": "0002", "player": ""}, {"round": "01", "pick": "05", "franchise": "0009", "player": ""}, {"round": "01", "pick": "06", "franchise": "0004", "player": ""}, {"round": "01", "pick": "07", "franchise": "0005", "player": ""}, {"round": "01", "pick": "08", "franchise": "0001", "player": ""}, {"round": "01", "pick": "09", "franchise": "0011", "player": ""}, {"round": "01", "pick": "10", "franchise": "0007", "player": ""}, {"round": "01", "pick": "11", "franchise": "0010", "player": ""}, {"round": "01", "pick": "12", "franchise": "0003", "player": ""}, {"round": "02", "pick": "01", "franchise": "0003", "player": ""}, {"round": "02", "pick": "02", "franchise": "0010", "player": ""}, {"round": "02", "pick": "03", "franchise": "0007", "player": ""}, {"round": "02", "pick": "04", "franchise": "0011", "player": ""}, {"round": "02", "pick": "05", "franchise": "0001", "player": ""}, {"round": "02", "pick": "06", "franchise": "0005", "player": ""}, {"round": "02", "pick": "07", "franchise": "0004", "player": ""}, {"round": "02", "pick": "08", "franchise": "0009", "player": ""}, {"round": "02", "pick": "09", "franchise": "0002", "player": ""}, {"round": "02", "pick": "10", "franchise": "0006", "player": ""}, {"round": "02", "pick": "11", "franchise": "0008", "player": ""}, {"round": "02", "pick": "12", "franchise": "0012", "player": ""}, {"round": "03", "pick": "01", "franchise": "0003", "player": ""}, {"round": "03", "pick": "02", "franchise": "0008", "player": ""}, {"round": "03", "pick": "03", "franchise": "0005", "player": ""}, {"round": "03", "pick": "04", "franchise": "0012", "player": ""}, {"round": "03", "pick": "05", "franchise": "0009", "player": ""}, {"round": "03", "pick": "06", "franchise": "0010", "player": ""}, {"round": "03", "pick": "07", "franchise": "0006", "player": ""}, {"round": "03", "pick": "08", "franchise": "0007", "player": ""}, {"round": "03", "pick": "09", "franchise": "0002", "player": ""}, {"round": "03", "pick": "10", "franchise": "0004", "player": ""}, {"round": "03", "pick": "11", "franchise": "0011", "player": ""}, {"round": "03", "pick": "12", "franchise": "0001", "player": ""}, {"round": "04", "pick": "01", "franchise": "0006", "player": ""}, {"round": "04", "pick": "02", "franchise": "0010", "player": ""}, {"round": "04", "pick": "03", "franchise": "0005", "player": ""}, {"round": "04", "pick": "04", "franchise": "0011", "player": ""}, {"round": "04", "pick": "05", "franchise": "0001", "player": ""}, {"round": "04", "pick": "06", "franchise": "0009", "player": ""}, {"round": "04", "pick": "07", "franchise": "0008", "player": ""}, {"round": "04", "pick": "08", "franchise": "0007", "player": ""}, {"round": "04", "pick": "09", "franchise": "0004", "player": ""}, {"round": "04", "pick": "10", "franchise": "0012", "player": ""}, {"round": "04", "pick": "11", "franchise": "0003", "player": ""}, {"round": "04", "pick": "12", "franchise": "0002", "player": ""}, {"round": "05", "pick": "01", "franchise": "0002", "player": ""}, {"round": "05", "pick": "02", "franchise": "0003", "player": ""}, {"round": "05", "pick": "03", "franchise": "0012", "player": ""}, {"round": "05", "pick": "04", "franchise": "0004", "player": ""}, {"round": "05", "pick": "05", "franchise": "0007", "player": ""}, {"round": "05", "pick": "06", "franchise": "0008", "player": ""}, {"round": "05", "pick": "07", "franchise": "0009", "player": ""}, {"round": "05", "pick": "08", "franchise": "0001", "player": ""}, {"round": "05", "pick": "09", "franchise": "0011", "player": ""}, {"round": "05", "pick": "10", "franchise": "0005", "player": ""}, {"round": "05", "pick": "11", "franchise": "0010", "player": ""}, {"round": "05", "pick": "12", "franchise": "0006", "player": ""}, {"round": "06", "pick": "01", "franchise": "0003", "player": ""}, {"round": "06", "pick": "02", "franchise": "0008", "player": ""}, {"round": "06", "pick": "03", "franchise": "0004", "player": ""}, {"round": "06", "pick": "04", "franchise": "0001", "player": ""}, {"round": "06", "pick": "05", "franchise": "0011", "player": ""}, {"round": "06", "pick": "06", "franchise": "0002", "player": ""}, {"round": "06", "pick": "07", "franchise": "0006", "player": ""}, {"round": "06", "pick": "08", "franchise": "0012", "player": ""}, {"round": "06", "pick": "09", "franchise": "0007", "player": ""}, {"round": "06", "pick": "10", "franchise": "0005", "player": ""}, {"round": "06", "pick": "11", "franchise": "0010", "player": ""}, {"round": "06", "pick": "12", "franchise": "0009", "player": ""}, {"round": "07", "pick": "01", "franchise": "0009", "player": ""}, {"round": "07", "pick": "02", "franchise": "0010", "player": ""}, {"round": "07", "pick": "03", "franchise": "0005", "player": ""}, {"round": "07", "pick": "04", "franchise": "0007", "player": ""}, {"round": "07", "pick": "05", "franchise": "0012", "player": ""}, {"round": "07", "pick": "06", "franchise": "0006", "player": ""}, {"round": "07", "pick": "07", "franchise": "0002", "player": ""}, {"round": "07", "pick": "08", "franchise": "0011", "player": ""}, {"round": "07", "pick": "09", "franchise": "0001", "player": ""}, {"round": "07", "pick": "10", "franchise": "0004", "player": ""}, {"round": "07", "pick": "11", "franchise": "0008", "player": ""}, {"round": "07", "pick": "12", "franchise": "0003", "player": ""}, {"round": "08", "pick": "01", "franchise": "0012", "player": ""}, {"round": "08", "pick": "02", "franchise": "0005", "player": ""}, {"round": "08", "pick": "03", "franchise": "0002", "player": ""}, {"round": "08", "pick": "04", "franchise": "0010", "player": ""}, {"round": "08", "pick": "05", "franchise": "0008", "player": ""}, {"round": "08", "pick": "06", "franchise": "0006", "player": ""}, {"round": "08", "pick": "07", "franchise": "0011", "player": ""}, {"round": "08", "pick": "08", "franchise": "0007", "player": ""}, {"round": "08", "pick": "09", "franchise": "0003", "player": ""}, {"round": "08", "pick": "10", "franchise": "0009", "player": ""}, {"round": "08", "pick": "11", "franchise": "0004", "player": ""}, {"round": "08", "pick": "12", "franchise": "0001", "player": ""}, {"round": "09", "pick": "01", "franchise": "0001", "player": ""}, {"round": "09", "pick": "02", "franchise": "0004", "player": ""}, {"round": "09", "pick": "03", "franchise": "0009", "player": ""}, {"round": "09", "pick": "04", "franchise": "0003", "player": ""}, {"round": "09", "pick": "05", "franchise": "0007", "player": ""}, {"round": "09", "pick": "06", "franchise": "0011", "player": ""}, {"round": "09", "pick": "07", "franchise": "0006", "player": ""}, {"round": "09", "pick": "08", "franchise": "0008", "player": ""}, {"round": "09", "pick": "09", "franchise": "0010", "player": ""}, {"round": "09", "pick": "10", "franchise": "0002", "player": ""}, {"round": "09", "pick": "11", "franchise": "0005", "player": ""}, {"round": "09", "pick": "12", "franchise": "0012", "player": ""}, {"round": "10", "pick": "01", "franchise": "0001", "player": ""}, {"round": "10", "pick": "02", "franchise": "0011", "player": ""}, {"round": "10", "pick": "03", "franchise": "0010", "player": ""}, {"round": "10", "pick": "04", "franchise": "0008", "player": ""}, {"round": "10", "pick": "05", "franchise": "0007", "player": ""}, {"round": "10", "pick": "06", "franchise": "0012", "player": ""}, {"round": "10", "pick": "07", "franchise": "0006", "player": ""}, {"round": "10", "pick": "08", "franchise": "0004", "player": ""}, {"round": "10", "pick": "09", "franchise": "0009", "player": ""}, {"round": "10", "pick": "10", "franchise": "0003", "player": ""}, {"round": "10", "pick": "11", "franchise": "0005", "player": ""}, {"round": "10", "pick": "12", "franchise": "0002", "player": ""}, {"round": "11", "pick": "01", "franchise": "0002", "player": ""}, {"round": "11", "pick": "02", "franchise": "0005", "player": ""}, {"round": "11", "pick": "03", "franchise": "0003", "player": ""}, {"round": "11", "pick": "04", "franchise": "0009", "player": ""}, {"round": "11", "pick": "05", "franchise": "0004", "player": ""}, {"round": "11", "pick": "06", "franchise": "0006", "player": ""}, {"round": "11", "pick": "07", "franchise": "0012", "player": ""}, {"round": "11", "pick": "08", "franchise": "0007", "player": ""}, {"round": "11", "pick": "09", "franchise": "0008", "player": ""}, {"round": "11", "pick": "10", "franchise": "0010", "player": ""}, {"round": "11", "pick": "11", "franchise": "0011", "player": ""}, {"round": "11", "pick": "12", "franchise": "0001", "player": ""}, {"round": "12", "pick": "01", "franchise": "0009", "player": ""}, {"round": "12", "pick": "02", "franchise": "0001", "player": ""}, {"round": "12", "pick": "03", "franchise": "0004", "player": ""}, {"round": "12", "pick": "04", "franchise": "0011", "player": ""}, {"round": "12", "pick": "05", "franchise": "0012", "player": ""}, {"round": "12", "pick": "06", "franchise": "0003", "player": ""}, {"round": "12", "pick": "07", "franchise": "0007", "player": ""}, {"round": "12", "pick": "08", "franchise": "0006", "player": ""}, {"round": "12", "pick": "09", "franchise": "0002", "player": ""}, {"round": "12", "pick": "10", "franchise": "0008", "player": ""}, {"round": "12", "pick": "11", "franchise": "0005", "player": ""}, {"round": "12", "pick": "12", "franchise": "0010", "player": ""}]}}}'

def fixture_js():
    import json as _j
    # chr(10) rather than an escape: generated-JS escapes keep getting eaten
    tag_close = "</scr" + "ipt>"
    return ("<script>window.MFL_FIXTURE = " + _j.dumps(MFL_FIXTURE) + ";"
            + tag_close + chr(10))

harness = r'''
<script>
(async function(){
  var log=[];
  function step(n,f){
    try{
      var r=f();
      /* A test that returns a promise would otherwise be logged ok before it ran -
         the same class of hollow assertion that let a dead switch ship. Refuse it. */
      if(r && typeof r.then === "function"){
        log.push(n+":FAIL async body passed to the sync step(); use astep()");
        return;
      }
      log.push(n+":ok");
    }catch(e){ log.push(n+":FAIL "+e.message); }
  }
  async function astep(n,f){
    try{ await f(); log.push(n+":ok"); }
    catch(e){ log.push(n+":FAIL "+(e && e.message || e)); }
  }

  /* Placeholders are global and persist in byId, so a test that creates them must put
     the world back or it changes every simulation that runs after it. */
  function clearPlaceholders(){
    OFFBOARD = new Map();
    state.picks = [];
    state.byLeague = {};
    applyLeague(state.league);
    state.picks = [];
  }

  function playOut(){
    var need=Math.min(state.teams*state.rounds,PLAYERS.length), g=0;
    runSim();
    while(state.picks.length<need && g++<600){
      var r=recommend(); if(!r.length) break;
      makePick(r[0].p.id); runSim();
    }
    return need;
  }
  function counts(t){
    var r=rosterOf(t), o={};
    ["QB","RB","WR","TE","PK","DEF"].forEach(function(p){
      o[p]=r.filter(function(x){return x.pos===p}).length; });
    return o;
  }
  /* applyLeague() wipes state.picks, so any test that inspects a roster must draft
     AFTER switching leagues. This does both in the right order. */
  function ensureDraft(league, slot){
    applyLeague(league);
    state.slot = slot || 1; state.sim = true; state.picks = []; reseed(); runSim();
    var need = Math.min(state.teams*state.rounds, PLAYERS.length), g = 0;
    while(state.picks.length < need && g++ < 600){
      var r = recommend(); if(!r.length) break;
      makePick(r[0].p.id); runSim();
    }
  }

  /* Switch league for a test that does not need a drafted roster. */
  function ensureLeagueOnly(league){ state.picks=[]; state.byLeague={}; applyLeague(league); }

  function boardCount(pos){
    return PLAYERS.filter(function(p){ return p.pos===pos; }).length;
  }
  /* A team can only be faulted for missing a position the board could actually
     supply. Where league-wide demand exceeds the ranked pool (CBS needs 12
     kickers; the non-PPR top 200 lists 10), the correct expectation is that the
     pool was drained, not that every team filled the slot. */
  function shortfall(c, reqs){
    var bad=[], drafted={};
    state.picks.forEach(function(pk){
      var p=byId.get(pk.playerId); drafted[p.pos]=(drafted[p.pos]||0)+1;
    });
    Object.keys(reqs).forEach(function(p){
      if(!reqs[p] || c[p]>=reqs[p]) return;
      var supply=boardCount(p);
      if(reqs[p]*state.teams > supply){
        if((drafted[p]||0) < supply) bad.push(p+" short but pool not drained ("+(drafted[p]||0)+"/"+supply+")");
        return;                                  // scarcity is the board's, not the app's
      }
      bad.push(p+" "+c[p]+"/"+reqs[p]);
    });
    return bad;
  }

  var KEYS=["espn10","cbs12","mfl12","sleeper12"];
  KEYS.forEach(function(LK){
    var tag="["+LK+"] ";
    step(tag+"apply",function(){
      applyLeague(LK);
      var L=LEAGUES[LK];
      if(state.teams!==L.teams) throw new Error("teams "+state.teams);
      if(state.rounds!==L.rounds) throw new Error("rounds "+state.rounds);
      (L.drop||[]).forEach(function(pos){
        if(PLAYERS.some(function(p){return p.pos===pos}))
          throw new Error(pos+" not dropped from pool");
      });
      if(state.teams*state.rounds > PLAYERS.length)
        throw new Error("pool too small: "+PLAYERS.length+" for "+(state.teams*state.rounds)+" picks");
    });

    step(tag+"plan-block",function(){
      var shown=[].slice.call(document.querySelectorAll(".planblock"))
        .filter(function(b){ return !b.hidden; });
      if(shown.length!==1||shown[0].dataset.league!==LK)
        throw new Error("shown="+shown.length+" "+(shown[0]&&shown[0].dataset.league));
    });

    step(tag+"snake",function(){
      for(var rd=0; rd<state.rounds; rd++)
        for(var col=0; col<state.teams; col++){
          var ov=rd*state.teams+((rd%2===0)?col:(state.teams-1-col));
          if(teamOnClock(ov)!==col) throw new Error("rd"+rd+" col"+col);
        }
    });

    step(tag+"ai-rosters-legal",function(){
      state.slot=1; state.sim=true; state.picks=[]; reseed();
      var need=playOut();
      if(state.picks.length!==need) throw new Error("stalled "+state.picks.length+"/"+need);
      for(var t=0;t<state.teams;t++){
        if(t===state.slot-1) continue;
        var bad=shortfall(counts(t), AI_NEED);
        if(bad.length) throw new Error("team"+(t+1)+" "+bad.join(","));
      }
    });

    step(tag+"my-roster-meets-full-need",function(){
      for(var sl=1; sl<=state.teams; sl+=3){
        state.slot=sl; state.sim=true; state.picks=[]; reseed(); playOut();
        var bad=shortfall(counts(sl-1), AI_NEED);
        if(bad.length) throw new Error("slot"+sl+" "+bad.join(","));
      }
    });

    step(tag+"no-early-K-or-DST",function(){
      if(!NEED.PK && !NEED.DEF){ return; }
      var lim=state.rounds-(Math.max(NEED.PK,NEED.DEF)+1);
      var bad=state.picks.filter(function(pk){
        var p=byId.get(pk.playerId);
        return (p.pos==="PK"||p.pos==="DEF") && roundOf(pk.overall)<lim;
      });
      if(bad.length) throw new Error(bad.length+" before round "+lim);
    });

    step(tag+"views",function(){
      renderBoard(); renderDraft(); renderTeam(); renderDepth(); renderIntel(); renderCliffs();
    });
  });

  step("off-board-warning-fires-only-when-the-board-is-short",function(){
    /* This used to assert CBS always shows the note, which was true only because the
       built-in board carried ten kickers against a 24-kicker requirement. The board
       now covers every league's minimums, so the honest test is that the note stays
       quiet when it should and still fires when it must. */
    ["espn10","cbs12","mfl12","sleeper12"].forEach(function(lg){
      applyLeague(lg);
      if(offBoardNote() !== "")
        throw new Error(lg+" warns about an off-board need the board can now cover");
    });
    /* Demand more than exists and it must speak up. */
    applyLeague("cbs12");
    var realTE = NEED.TE;
    NEED.TE = 40;                       // 480 tight ends across 12 teams
    var note = offBoardNote();
    NEED.TE = realTE;
    if(note.indexOf("off the board") < 0)
      throw new Error("no warning when the board genuinely cannot cover the rules");
    applyLeague("cbs12");
  });




  step("projections-attached",function(){
    var keys=["espn10","cbs12","mfl12","sleeper12"], out=[];
    keys.forEach(function(k){
      applyLeague(k);
      var withProj=PLAYERS.filter(function(p){return p.proj!==null}).length;
      var pct=Math.round(withProj/PLAYERS.length*100);
      if(pct<85) throw new Error(k+" only "+pct+"% have projections");
      out.push(k+" "+pct+"%");
    });
    log.push("   ("+out.join(", ")+")");
  });

  step("scoring-differs-by-league",function(){
    applyLeague("espn10");
    var e=PLAYERS.find(function(p){return p.name==="Josh Allen"});
    var espnPts=e.proj;
    applyLeague("cbs12");
    var c=PLAYERS.find(function(p){return p.name==="Josh Allen"});
    if(!(c.proj>espnPts+30))
      throw new Error("6pt pass TD should lift Allen well above "+espnPts+", got "+c.proj);
    applyLeague("sleeper12");
    var s=PLAYERS.find(function(p){return p.name==="Puka Nacua"});
    applyLeague("espn10");
    var s2=PLAYERS.find(function(p){return p.name==="Puka Nacua"});
    if(!(s.proj>s2.proj+80)) throw new Error("PPR should lift Nacua ~107 pts over standard");
    log.push("   (Allen "+espnPts+" ESPN vs "+c.proj+" CBS; Nacua "+s2.proj+" std vs "+s.proj+" PPR)");
  });

  step("vorp-is-sane",function(){
    applyLeague("sleeper12");
    var qb=PLAYERS.filter(function(p){return p.pos==="QB"&&p.vorp!==null})
                  .sort(function(a,b){return b.vorp-a.vorp});
    var rb=PLAYERS.filter(function(p){return p.pos==="RB"&&p.vorp!==null})
                  .sort(function(a,b){return b.vorp-a.vorp});
    if(!qb.length||!rb.length) throw new Error("no vorp computed");
    if(qb[0].vorp<=0) throw new Error("top QB vorp not positive");
    /* Superflex does NOT automatically make the best QB the most valuable asset —
       QB scoring is compressed, so the gap from QB1 to replacement is smaller than
       RB1 to replacement even when 24 QBs start. What superflex must do is lift the
       position sharply relative to a one-QB league; that is what we assert. */
    window.__sfQb = qb[0].vorp;
    log.push("   (SF top QB "+qb[0].name+" +"+qb[0].vorp+" vs top RB "+rb[0].name+" +"+rb[0].vorp+")");
  });

  step("vorp-flips-in-single-qb",function(){
    applyLeague("espn10");
    var qb=PLAYERS.filter(function(p){return p.pos==="QB"&&p.vorp!==null})
                  .sort(function(a,b){return b.vorp-a.vorp});
    var rb=PLAYERS.filter(function(p){return p.pos==="RB"&&p.vorp!==null})
                  .sort(function(a,b){return b.vorp-a.vorp});
    if(qb[0].vorp >= rb[0].vorp)
      throw new Error("1QB league: QB vorp "+qb[0].vorp+" should trail RB "+rb[0].vorp);
    if(!(window.__sfQb > qb[0].vorp * 1.5))
      throw new Error("superflex should lift top-QB value well above the 1QB league: "+
                      window.__sfQb+" vs "+qb[0].vorp);
    log.push("   (top QB VORP: "+qb[0].vorp+" in 1QB vs "+window.__sfQb+" in superflex; top RB +"+rb[0].vorp+")");
  });


  step("sorting-by-value",function(){
    applyLeague("espn10");
    state.sortBy="vorp"; renderBoard();
    var names=[].slice.call(document.querySelectorAll("#boardBody .pname")).map(function(e){return e.textContent});
    if(names.length<10) throw new Error("board empty");
    var byV=PLAYERS.filter(function(p){return p.vorp!==null}).sort(function(a,b){return b.vorp-a.vorp});
    if(names[0]!==byV[0].name) throw new Error("top row "+names[0]+" != best value "+byV[0].name);
    state.sortBy="adp"; renderBoard();
    var first=document.querySelector("#boardBody .pname").textContent;
    if(first!==PLAYERS[0].name) throw new Error("ADP sort broken: "+first);
    log.push("   (best value in ESPN: "+byV[0].name+" +"+byV[0].vorp+")");
  });

  step("injury-badges-render",function(){
    applyLeague("espn10");
    // inject a status the way the live feed would, then confirm it surfaces
    var p=PLAYERS[0]; var saved=p.inj; p.inj="Questionable";
    renderBoard();
    var html=document.getElementById("boardBody").innerHTML;
    p.inj=saved; renderBoard();
    if(html.indexOf(">Q<")<0) throw new Error("no injury badge rendered");
  });

  step("injured-players-demoted",function(){
    applyLeague("espn10"); state.picks=[]; state.sim=false; state.slot=1;
    var before=recommend()[0].p;
    before.inj="Out";
    var after=recommend();
    var pos=after.map(function(r){return r.p.id}).indexOf(before.id);
    before.inj="";
    if(pos===0) throw new Error("an OUT player still ranks first");
  });

  step("live-merge-uses-fetched-rows",function(){
    applyLeague("sleeper12");
    var target=PLAYERS.find(function(p){return p.pos==="WR"&&p.proj!==null});
    var baseline=target.proj;
    LIVEDATA=liveRowsToMaps([{name:target.name,pos:"WR",team:target.team,gp:18,
      passYd:0,passTd:0,int:0,rushYd:0,rushTd:0,rec:200,recYd:3000,recTd:30,fum:0,
      sleeperPts:0,adpStd:1,adpPpr:1,adp2qb:1,inj:"Questionable"}], Date.now());
    applyLeague("sleeper12");
    var after=PLAYERS.find(function(p){return p.name===target.name});
    if(!(after.proj>baseline+200)) throw new Error("live row ignored ("+baseline+" -> "+after.proj+")");
    if(after.inj!=="Questionable") throw new Error("injury not carried over");
    LIVEDATA=null; applyLeague("sleeper12");
    var back=PLAYERS.find(function(p){return p.name===target.name});
    if(Math.abs(back.proj-baseline)>0.5) throw new Error("did not fall back to snapshot");
    log.push("   (live merge + fallback verified on "+target.name+")");
  });

  step("kickers-and-defenses-have-projections",function(){
    ["espn10","cbs12","mfl12"].forEach(function(k){
      applyLeague(k);
      var ks=PLAYERS.filter(function(p){return p.pos==="PK"});
      var ds=PLAYERS.filter(function(p){return p.pos==="DEF"});
      var kOk=ks.filter(function(p){return p.proj!==null}).length;
      var dOk=ds.filter(function(p){return p.proj!==null}).length;
      if(ks.length && kOk===0) throw new Error(k+": 0 of "+ks.length+" kickers have projections");
      if(ds.length && dOk===0) throw new Error(k+": 0 of "+ds.length+" defenses have projections");
      if(ks.length && kOk<ks.length*0.8) throw new Error(k+" kickers only "+kOk+"/"+ks.length);
    });
    applyLeague("espn10");
    var k=PLAYERS.filter(function(p){return p.pos==="PK"&&p.proj!==null})
                 .sort(function(a,b){return b.proj-a.proj})[0];
    log.push("   (top kicker "+k.name+" "+k.proj+" pts)");
  });

  step("every-position-has-coverage",function(){
    applyLeague("cbs12");
    ["QB","RB","WR","TE","PK","DEF"].forEach(function(pos){
      var all=PLAYERS.filter(function(p){return p.pos===pos});
      if(!all.length) return;
      var ok=all.filter(function(p){return p.proj!==null}).length;
      if(ok/all.length < 0.7) throw new Error(pos+" coverage "+ok+"/"+all.length);
    });
  });


  step("draft-id-is-device-local",function(){
    applyLeague("sleeper12");
    // split so this probe does not match itself in the harness source
    var probe = "13897040" + "38232121345";
    if(document.documentElement.innerHTML.indexOf(probe) >= 0)
      throw new Error("a draft id is still baked into the page");
    setDraftId("sleeper12","");
    if(draftIdFor("sleeper12")!=="") throw new Error("clear failed");
    refreshBookmarklet("sleeper12");
    if(document.getElementById("bmCode").value.indexOf("Enter your draft ID")<0)
      throw new Error("bookmarklet should prompt when no id is set");
    setDraftId("sleeper12","999888777");
    applyLeague("sleeper12");
    var bm=document.getElementById("bmCode").value;
    if(bm.indexOf("999888777")<0) throw new Error("bookmarklet did not pick up the saved id");
    if(document.getElementById("draftIdIn").value!=="999888777")
      throw new Error("settings field not repopulated");
    setDraftId("sleeper12","");
  });

  step("labels-carry-no-league-identity",function(){
    var bad=/Chewey|SWFFL|Siena|My 2026 League/i;
    Object.keys(LEAGUES).forEach(function(k){
      if(bad.test(LEAGUES[k].label)) throw new Error(k+" label still identifies the league");
    });
    if(bad.test(document.getElementById("p-plan").innerHTML))
      throw new Error("plan text still names a league");
  });


  step("sos-computed-for-all-32",function(){
    applyLeague("espn10");
    var t=Object.keys(SOS);
    if(t.length!==32) throw new Error("SOS for "+t.length+" teams");
    var bad=t.filter(function(x){return SOS[x].season===null||SOS[x].playoff===null});
    if(bad.length) throw new Error("null SOS: "+bad.join(","));
    var ranks=t.map(function(x){return SOS[x].playoffRank}).sort(function(a,b){return a-b});
    if(ranks[0]!==1||ranks[31]!==32) throw new Error("rank range "+ranks[0]+"-"+ranks[31]);
  });

  step("schedule-agrees-with-bye-table",function(){
    var wrong=[];
    Object.keys(SCHEDULE).forEach(function(t){
      var byeIdx=SCHEDULE[t].indexOf("");
      var derived=byeIdx>=0?byeIdx+1:null;
      if(BYES[t]!==derived) wrong.push(t+" table="+BYES[t]+" schedule="+derived);
    });
    if(wrong.length) throw new Error(wrong.slice(0,4).join("; "));
    log.push("   (all 32 byes cross-check against the schedule)");
  });

  step("playoff-weeks-change-the-ranking",function(){
    applyLeague("espn10");                    // weeks 16-17
    var a=Object.keys(SOS).map(function(t){return t+SOS[t].playoffRank}).join();
    applyLeague("cbs12");                     // weeks 15-17
    var b=Object.keys(SOS).map(function(t){return t+SOS[t].playoffRank}).join();
    if(a===b) throw new Error("different playoff weeks produced identical ranks");
    var w=LEAGUES.espn10.playoffWeeks;
    if(w.length!==2||w[0]!==16) throw new Error("espn playoff weeks wrong: "+w);
  });

  step("sos-renders",function(){
    applyLeague("cbs12");
    renderSOS(); renderBoard(); renderDepth();
    if(document.getElementById("sosOut").innerHTML.indexOf("softest")<0)
      throw new Error("plan SOS block empty");
    if(document.getElementById("boardBody").innerHTML.indexOf("of 32, 1 = easiest")<0)
      throw new Error("board SOS column missing");
    if(document.getElementById("depthOut").innerHTML.indexOf("season")<0)
      throw new Error("depth card SOS missing");
  });


  step("slot-planner-runs-and-restores",function(){
    applyLeague("espn10");
    state.slot=4; state.sim=true; state.picks=[]; reseed(); runSim();
    var before=state.picks.length, seedBefore=state.seed, slotBefore=state.slot;
    var agg=slotReport(4, 6);
    if(state.picks.length!==before) throw new Error("planner clobbered the live draft");
    if(state.slot!==slotBefore || state.seed!==seedBefore) throw new Error("planner clobbered state");
    var rounds=Object.keys(agg).map(Number).sort(function(a,b){return a-b});
    if(rounds[0]!==1) throw new Error("no round 1 data");
    if(rounds.length < state.rounds-2) throw new Error("only "+rounds.length+" rounds planned");
    var r1=agg[1];
    if(r1.n!==6) throw new Error("round 1 sampled "+r1.n+" times, expected 6");
  });

  step("slot-planner-differs-by-seat",function(){
    applyLeague("espn10");
    function firstPos(slot){
      var a=slotReport(slot, 8)[1].pos;
      return Object.keys(a).sort(function(x,y){return a[y]-a[x]})[0];
    }
    var early=slotReport(1, 8)[1], late=slotReport(10, 8)[1];
    var eName=Object.keys(slotReport(1,8)[1].name).length;
    // seat 1 and seat 10 should not produce identical round-1 name distributions
    var n1=Object.keys(slotReport(1,8)[1].name).join(),
        n10=Object.keys(slotReport(10,8)[1].name).join();
    if(n1===n10) throw new Error("seat 1 and seat 10 saw the same round-1 board");
    log.push("   (slot planner: seat 1 vs seat 10 differ in round 1)");
  });

  step("slot-planner-respects-roster-rules",function(){
    applyLeague("cbs12");
    var agg=slotReport(6, 6);
    var kRounds=Object.keys(agg).filter(function(r){ return agg[r].pos.PK; }).map(Number);
    if(kRounds.length && Math.min.apply(null,kRounds) < state.rounds-3)
      throw new Error("planner drafted a kicker in round "+Math.min.apply(null,kRounds));
  });


  step("replacement-uses-starters-not-roster-minimums",function(){
    applyLeague("cbs12");
    // CBS: roster 2 QB but START 1. Replacement must be QB12, not QB24.
    if(Math.abs(STARTERS.QB-1)>0.01) throw new Error("CBS QB starters = "+STARTERS.QB);
    if(Math.abs(STARTERS.TE-1)>0.01) throw new Error("CBS TE starters = "+STARTERS.TE);
    var qbs=PLAYERS.filter(function(p){return p.pos==="QB"&&p.proj!==null})
                   .sort(function(a,b){return b.proj-a.proj});
    if(Math.abs(REPLACEMENT.QB-qbs[11].proj)>0.01)
      throw new Error("QB replacement should be QB12 ("+qbs[11].proj+"), got "+REPLACEMENT.QB);
    log.push("   (CBS QB replacement now QB12 "+qbs[11].proj+", was QB24)");
  });

  step("superflex-still-values-two-QBs",function(){
    applyLeague("sleeper12");
    // QB1 dedicated + 0.85 of the superflex = ~1.85 starting QBs per team
    if(STARTERS.QB < 1.5) throw new Error("superflex QB starters only "+STARTERS.QB);
    applyLeague("espn10");
    if(STARTERS.QB > 1.05) throw new Error("1QB league starters "+STARTERS.QB);
  });

  step("mfl-tight-ends-are-flex-valued",function(){
    applyLeague("mfl12");
    if(STARTERS.TE<=0) throw new Error("MFL TE starters should come from the flex, got "+STARTERS.TE);
    var te=PLAYERS.filter(function(p){return p.pos==="TE"&&p.vorp!==null});
    if(!te.length) throw new Error("MFL tight ends have no value at all");
  });

  step("planner-no-longer-hoards-one-position",function(){
    applyLeague("cbs12");
    var agg=slotReport(5, 10);
    var counts={};
    Object.keys(agg).forEach(function(r){
      if(Number(r)>8) return;
      Object.keys(agg[r].pos).forEach(function(pos){
        counts[pos]=(counts[pos]||0)+agg[r].pos[pos]/agg[r].n;
      });
    });
    Object.keys(counts).forEach(function(pos){
      if(pos==="RB"||pos==="WR") return;
      if(counts[pos] > 2.6)
        throw new Error("planner takes "+counts[pos].toFixed(1)+" "+pos+" in the first 8 rounds");
    });
    log.push("   (first-8-round mix: "+Object.keys(counts).map(function(p){
      return p+" "+counts[p].toFixed(1); }).join(", ")+")");
  });


  step("survival-behaves-like-a-probability",function(){
    applyLeague("espn10"); state.picks=[];
    var p=PLAYERS[20];
    var a=survival(p, 10, 20), b=survival(p, 10, 40), c=survival(p, 10, 80);
    [a,b,c].forEach(function(v){ if(v<0||v>1) throw new Error("out of range: "+v); });
    if(!(a>=b && b>=c)) throw new Error("not monotonic: "+a+" "+b+" "+c);
    if(survival(p, 10, null)!==1) throw new Error("no next pick should be certain");
    if(survival(p, 10, 5)!==1) throw new Error("a pick in the past should be certain");
    // someone going far later should be very likely to survive a short wait
    var late=PLAYERS[150];
    if(survival(late, 5, 12) < 0.9) throw new Error("late-ADP player should survive a short gap");
    // the very best player should rarely survive a long one
    if(survival(PLAYERS[0], 1, 25) > 0.15) throw new Error("elite player survives too easily");
    log.push("   (survival: p21 to +10/+30/+70 picks = "+
      Math.round(a*100)+"%/"+Math.round(b*100)+"%/"+Math.round(c*100)+"%)");
  });

  step("cost-of-waiting-is-sane",function(){
    applyLeague("espn10"); state.picks=[];
    var rows=costOfWaiting(available(), 1, 20);
    if(!rows.length) throw new Error("no positions returned");
    rows.forEach(function(r){
      if(r.drop < -0.01) throw new Error(r.pos+" has negative cost "+r.drop);
      if(r.best.vorp < r.expected.vorp-0.01)
        throw new Error(r.pos+" expected player beats the best available");
    });
    if(!rows.every(function(r,i,arr){ return i===0 || arr[i-1].drop >= r.drop; }))
      throw new Error("not sorted by cost");
    log.push("   (cost of waiting from pick 1 to 20: "+
      rows.slice(0,3).map(function(r){return r.pos+" -"+r.drop.toFixed(0)}).join(", ")+")");
  });

  step("scarcity-shifts-recommendations",function(){
    applyLeague("espn10"); state.slot=1; state.sim=true; state.picks=[]; reseed(); runSim();
    var recs=recommend();
    if(!recs.length) throw new Error("no recommendations");
    var withOdds=recs.filter(function(r){ return r.p._surv!==undefined; });
    if(withOdds.length!==recs.length) throw new Error("survival not attached to every rec");
    renderDraft();
    if(document.getElementById("recs").innerHTML.indexOf("to last")<0)
      throw new Error("odds not shown in the UI");
    if(document.getElementById("cowOut").innerHTML.indexOf("Value lost")<0)
      throw new Error("cost-of-waiting card empty");
  });

  step("adp-disagreement-flagged",function(){
    applyLeague("espn10");
    var t=PLAYERS.find(function(p){return p.pos==="WR"});
    LIVEDATA=liveRowsToMaps([{name:t.name,pos:"WR",team:t.team,gp:18,passYd:0,passTd:0,int:0,
      rushYd:0,rushTd:0,rec:80,recYd:1000,recTd:6,fum:0,sleeperPts:120,
      adpStd:t.adp+60, adpPpr:t.adp+60, adp2qb:t.adp+60, inj:""}], Date.now());
    state.useLiveAdp=false; applyLeague("espn10");
    var after=PLAYERS.find(function(p){return p.name===t.name});
    if(after.adpAlt===null) throw new Error("alternate ADP not captured");
    if(adpGapNote(after).indexOf("falls")<0) throw new Error("no disagreement badge");
    LIVEDATA=null; applyLeague("espn10");
    var back=PLAYERS.find(function(p){return p.name===t.name});
    if(adpGapNote(back)!=="") throw new Error("badge should vanish without live data");
  });


  step("week-view-scores-and-fills-lineup",function(){
    applyLeague("espn10"); state.slot=1; state.sim=true; state.picks=[]; reseed();
    var need=Math.min(state.teams*state.rounds,PLAYERS.length), g=0; runSim();
    while(state.picks.length<need && g++<600){ var r=recommend(); if(!r.length) break; makePick(r[0].p.id); runSim(); }
    // stand in for the network with a synthetic week
    var rows=new Map(), defs=new Map();
    rosterOf(myIdx()).forEach(function(p,i){
      var row={name:p.name,pos:p.pos,team:p.team,opp:"XX",passYd:0,passTd:0,int:0,
        rushYd:60+i,rushTd:0,rec:4,recYd:40,recTd:0,fum:0,sleeperPts:8+i,inj:""};
      if(p.pos==="DEF") defs.set(p.team,row); else rows.set(normName(p.name)+"|"+p.pos,row);
    });
    WEEKLY={week:3, byName:rows, byDefTeam:defs, at:Date.now()};
    state.tab="week"; document.getElementById("p-week").hidden=false;
    renderWeek();
    var html=document.getElementById("weekOut").innerHTML;
    if(html.indexOf("Week 3 lineup")<0) throw new Error("lineup header missing");
    if(html.indexOf("projected")<0) throw new Error("no projected total");
    if(html.indexOf("Waiver targets")<0) throw new Error("no waiver section");
    WEEKLY=null;
  });

  step("week-lineup-is-optimal",function(){
    applyLeague("espn10");
    // two RBs, one clearly better; the better one must start
    var rbs=PLAYERS.filter(function(p){return p.pos==="RB"}).slice(0,2);
    state.picks=[]; state.sim=false; state.slot=1;
    var rows=new Map();
    rows.set(normName(rbs[0].name)+"|RB",{name:rbs[0].name,pos:"RB",team:rbs[0].team,opp:"AA",
      passYd:0,passTd:0,int:0,rushYd:50,rushTd:0,rec:0,recYd:0,recTd:0,fum:0,sleeperPts:5,inj:""});
    rows.set(normName(rbs[1].name)+"|RB",{name:rbs[1].name,pos:"RB",team:rbs[1].team,opp:"BB",
      passYd:0,passTd:0,int:0,rushYd:250,rushTd:3,rec:0,recYd:0,recTd:0,fum:0,sleeperPts:30,inj:""});
    // both must land on MY roster; makePick follows the clock, so assign directly
    state.picks.push({playerId:rbs[0].id, team:myIdx(), overall:0});
    state.picks.push({playerId:rbs[1].id, team:myIdx(), overall:1});
    WEEKLY={week:5, byName:rows, byDefTeam:new Map(), at:Date.now()};
    renderWeek();
    var html=document.getElementById("weekOut").innerHTML;
    var startBlock=html.slice(0, html.indexOf("Bench"));
    if(startBlock.indexOf(rbs[1].name)<0)
      throw new Error("the higher-scoring back is not in the lineup");
    WEEKLY=null; state.picks=[];
  });


  step("draft-date-is-device-local",function(){
    applyLeague("sleeper12");
    setDraftId("sleeper12","1234567890");
    setDraftWhen("sleeper12","2026-08-28T18:30");
    if(draftIdFor("sleeper12")!=="1234567890") throw new Error("id lost when date was set");
    if(draftWhenFor("sleeper12")!=="2026-08-28T18:30") throw new Error("date not stored");
    var c=draftCountdown("sleeper12");
    if(!c) throw new Error("no countdown");
    if(typeof c.hours!=="number") throw new Error("countdown malformed");
    // saving the id again must not wipe the date
    setDraftId("sleeper12","1234567890");
    if(draftWhenFor("sleeper12")!=="2026-08-28T18:30") throw new Error("date wiped by id save");
    setDraftId("sleeper12",""); setDraftWhen("sleeper12","");
  });

  step("draft-grade-ranks-the-room",function(){
    applyLeague("espn10"); state.slot=3; state.sim=true; state.picks=[]; reseed();
    var need=state.teams*state.rounds, g=0; renderAll();
    runSim();
    while(state.picks.length<need && g++<600){ var r=recommend(); if(!r.length) break; makePick(r[0].p.id); runSim(); }
    var pts=[];
    for(var t=0;t<state.teams;t++) pts.push(bestLineup(rosterOf(t)).points);
    if(pts.some(function(v){ return !(v>0); })) throw new Error("a roster scored nothing");
    renderTeam();
    var html=document.getElementById("teamOut").textContent;
    if(html.indexOf("Draft grade")<0) throw new Error("no grade shown");
    if(!/\d+ of 10/.test(html)) throw new Error("rank not rendered");
    var spread=Math.max.apply(null,pts)-Math.min.apply(null,pts);
    if(spread<=0) throw new Error("every roster identical - grade is meaningless");
    log.push("   (draft grade spread across 10 teams: "+spread.toFixed(0)+" pts)");
  });

  step("bye-outlook-counts-starters",function(){
    applyLeague("espn10");           // note: this clears picks, so draft a roster first
    state.slot=3; state.sim=true; state.picks=[]; reseed(); runSim();
    var need=state.teams*state.rounds, g=0;
    while(state.picks.length<need && g++<600){ var r=recommend(); if(!r.length) break; makePick(r[0].p.id); runSim(); }
    var out=byeOutlook(rosterOf(myIdx()));
    if(out.weeks.length!==18) throw new Error("expected 18 weeks");
    var total=out.weeks.reduce(function(a,w){ return a+w.off; },0);
    if(total!==out.starters)
      throw new Error("every starter has exactly one bye: "+total+" vs "+out.starters);
    renderTeam();
    if(document.getElementById("teamOut").textContent.indexOf("Bye outlook")<0)
      throw new Error("bye strip missing");
  });

  step("grade-hidden-early",function(){
    applyLeague("espn10"); state.picks=[]; state.sim=false;
    if(draftGrade()!=="") throw new Error("grade shown before the draft has run");
    if(byeStrip()!=="") throw new Error("bye strip shown with no roster");
  });


  step("trade-judged-on-starting-lineup",function(){
    applyLeague("espn10");
    state.slot=2; state.sim=true; state.picks=[]; reseed(); runSim();
    var need=state.teams*state.rounds, g=0;
    while(state.picks.length<need && g++<600){ var r=recommend(); if(!r.length) break; makePick(r[0].p.id); runSim(); }
    state.tradeOut.clear(); state.tradeIn.clear();
    if(evaluateTrade()!==null) throw new Error("empty trade should evaluate to nothing");

    // send my worst bench player, receive the best player on another roster
    var mine=rosterOf(myIdx()).slice().sort(function(a,b){
      return (a.vorp===null?-99:a.vorp)-(b.vorp===null?-99:b.vorp); });
    var theirs=rosterOf(myIdx()===0?1:0).slice().sort(function(a,b){
      return (b.vorp===null?-99:b.vorp)-(a.vorp===null?-99:a.vorp); });
    state.tradeOut.add(mine[0].id);
    state.tradeIn.add(theirs[0].id);
    var ev=evaluateTrade();
    if(!ev) throw new Error("no evaluation");
    if(ev.startersDelta <= 0)
      throw new Error("swapping my worst for their best should help: "+ev.startersDelta);
    if(ev.vorDelta <= 0) throw new Error("value should rise too");
    log.push("   (trade: worst-for-best = +"+ev.startersDelta.toFixed(0)+" starters, +"+ev.vorDelta.toFixed(0)+" value)");
    state.tradeOut.clear(); state.tradeIn.clear();
  });

  step("trade-spots-depth-that-does-not-start",function(){
    ensureDraft("espn10", 2);
    // receive a good player at a position where I already start the best available
    var qbs=rosterOf(myIdx()).filter(function(p){return p.pos==="QB"});
    if(!qbs.length) throw new Error("expected a QB on the roster after a full draft");
    var otherQb=PLAYERS.filter(function(p){
      return p.pos==="QB" && rosterOf(myIdx()).indexOf(p)<0 && p.vorp!==null;
    }).sort(function(a,b){return b.vorp-a.vorp})[0];
    if(!otherQb) return;
    state.tradeOut.clear(); state.tradeIn.clear();
    state.tradeIn.add(otherQb.id);
    var ev=evaluateTrade();
    if(ev.vorDelta<=0) throw new Error("getting a player for free should add value");
    if(ev.countDelta!==1) throw new Error("roster should grow by one");
    state.tradeIn.clear();
  });

  step("trade-flags-an-illegal-roster",function(){
    ensureDraft("espn10", 2);
    state.tradeOut.clear(); state.tradeIn.clear();
    var mineQb=rosterOf(myIdx()).filter(function(p){return p.pos==="QB"});
    if(!mineQb.length) throw new Error("no QB to trade away");
    mineQb.forEach(function(p){ state.tradeOut.add(p.id); });
    var ev=evaluateTrade();
    if(!ev) throw new Error("evaluation returned nothing");
    if(!ev.shortfalls.length) throw new Error("trading every QB should be flagged illegal");
    state.tradeOut.clear();
  });

  step("trade-panel-renders",function(){
    applyLeague("espn10");
    state.slot=2; state.sim=true; state.picks=[]; reseed(); runSim();
    var need=state.teams*state.rounds, g=0;
    while(state.picks.length<need && g++<600){ var r=recommend(); if(!r.length) break; makePick(r[0].p.id); runSim(); }
    state.tab="team"; document.getElementById("p-team").hidden=false;
    renderTeam();
    var html=document.getElementById("tradeOut").innerHTML;
    if(html.indexOf("You send")<0) throw new Error("trade panel not rendered");
    if(html.indexOf("You receive")<0) throw new Error("receive side missing");
  });

  step("each-league-keeps-its-own-draft",function(){
    /* Sleeper and ESPN draft the same evening, ESPN by hand. Switching between them
       must not destroy either board. */
    /* Clear the live board FIRST: applyLeague stashes whatever is currently on it,
       so wiping byLeague alone just lets the outgoing draft repopulate it. */
    state.picks = []; state.byLeague = {};
    ensureDraft("sleeper12", 5);
    var sleeperPicks = state.picks.length;
    var sleeperFirst = byId.get(state.picks[0].playerId).name;
    if(!sleeperPicks) throw new Error("no sleeper draft to preserve");

    applyLeague("espn10");
    if(state.picks.length !== 0) throw new Error("espn should start empty, got "+state.picks.length);
    state.sim = false;
    var espnTarget = PLAYERS[3];
    makePick(espnTarget.id);
    var espnPicks = state.picks.length;

    applyLeague("sleeper12");
    if(state.picks.length !== sleeperPicks)
      throw new Error("sleeper draft lost: "+state.picks.length+" of "+sleeperPicks);
    if(byId.get(state.picks[0].playerId).name !== sleeperFirst)
      throw new Error("sleeper board came back wrong");

    applyLeague("espn10");
    if(state.picks.length !== espnPicks) throw new Error("espn draft lost");
    if(byId.get(state.picks[0].playerId).name !== espnTarget.name)
      throw new Error("espn board came back wrong");
    log.push("   (sleeper "+sleeperPicks+" + espn "+espnPicks+" picks both survive switching)");
  });

  step("stale-ids-are-dropped-on-restore",function(){
    state.picks = []; state.byLeague = {};
    ensureDraft("espn10", 1);
    stashLeague();                    // make sure there is something to corrupt
    state.byLeague["espn10"].picks.push({playerId: 999999, team:0, overall:9999});
    applyLeague("sleeper12");
    applyLeague("espn10");
    if(state.picks.some(function(pk){ return !byId.has(pk.playerId); }))
      throw new Error("an invalid player id survived the restore");
  });

  step("draft-calendar-flags-the-overlap",function(){
    setDraftWhen("sleeper12","2026-08-28T18:30");
    setDraftWhen("espn10","2026-08-28T19:30");
    setDraftWhen("mfl12","2026-08-29T12:30");
    var d=draftClashes();
    if(d.all.length<3) throw new Error("only "+d.all.length+" dates read back");
    if(!d.clash.length) throw new Error("the two 28 Aug drafts should clash");
    renderDraftDiary();
    var html=document.getElementById("diaryOut").innerHTML;
    if(html.indexOf("Overlapping drafts")<0) throw new Error("no clash warning rendered");
    if(html.indexOf("manual entry")<0) throw new Error("offline league not marked manual");
    log.push("   (calendar: "+d.all.length+" drafts, "+d.clash.length+" overlap)");
  });


  step("fuzzy-search-finds-players-fast",function(){
    ensureLeagueOnly("espn10");
    var cases = [
      ["gibbs","Jahmyr Gibbs"], ["nacua","Puka Nacua"], ["jsn","Jaxon Smith-Njigba"],
      ["bijan","Bijan Robinson"], ["mccaff","Christian McCaffrey"],
      ["harrison","Marvin Harrison Jr."], ["cook","James Cook III"]
    ];
    cases.forEach(function(c){
      var hit = searchAvailable(c[0], 1)[0];
      if(!hit) throw new Error("no match for '"+c[0]+"'");
      if(hit.name !== c[1]) throw new Error("'"+c[0]+"' -> "+hit.name+", expected "+c[1]);
    });
    if(searchAvailable("", 5).length !== 0) throw new Error("empty query should match nothing");
    if(searchAvailable("zzzzzz", 5).length !== 0) throw new Error("nonsense matched something");
    log.push("   (fuzzy search: "+cases.length+" shorthand queries all resolve)");
  });

  step("search-skips-drafted-players",function(){
    ensureLeagueOnly("espn10");
    state.sim=false; state.picks=[];
    var g = searchAvailable("gibbs",1)[0];
    makePick(g.id);
    var again = searchAvailable("gibbs",1)[0];
    if(again && again.id === g.id) throw new Error("a drafted player still appears in search");
  });

  step("queue-shows-only-available-stars",function(){
    ensureLeagueOnly("espn10");
    state.sim=false; state.picks=[]; state.star.clear();
    var a=PLAYERS[0], b=PLAYERS[1], c=PLAYERS[2];
    [a,b,c].forEach(function(p){ state.star.add(p.id); });
    state.tab="draft"; document.getElementById("p-draft").hidden=false;
    renderDraft();
    var html=document.getElementById("queueOut").innerHTML;
    if(html.indexOf(a.name)<0) throw new Error("queued player missing");
    makePick(a.id);
    renderDraft();
    html=document.getElementById("queueOut").innerHTML;
    var pos=html.indexOf("Taken:");
    if(pos<0) throw new Error("drafted star not moved to Taken");
    if(html.slice(0,pos).indexOf(a.name)>=0) throw new Error("drafted star still listed as available");
    state.star.clear();
  });

  step("enter-key-drafts-top-match",function(){
    ensureLeagueOnly("espn10");
    state.sim=false; state.picks=[];
    state.tab="draft"; document.getElementById("p-draft").hidden=false; renderDraft();
    var box=document.getElementById("dsearch");
    box.value="jeanty"; box.focus();
    var before=state.picks.length;
    document.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}));
    if(state.picks.length!==before+1) throw new Error("Enter did not draft");
    var last=byId.get(state.picks[state.picks.length-1].playerId);
    if(last.name.indexOf("Jeanty")<0) throw new Error("wrong player drafted: "+last.name);
    if(box.value!=="") throw new Error("search box not cleared for the next pick");
  });

  step("digit-keys-draft-recommendations",function(){
    ensureLeagueOnly("espn10");
    state.sim=false; state.picks=[]; state.tab="draft";
    document.getElementById("p-draft").hidden=false; renderDraft();
    /* digits are for the recommendation list, but only when you are NOT typing a
       name - so make sure the search box does not still hold focus */
    var sb=document.getElementById("dsearch"); if(sb) sb.blur();
    if(document.activeElement && document.activeElement.tagName==="INPUT")
      document.activeElement.blur();
    var btns=document.querySelectorAll("#recs [data-draft]");
    if(!btns.length) throw new Error("no recommendations to key against");
    var target=+btns[1].dataset.draft;
    document.dispatchEvent(new KeyboardEvent("keydown",{key:"2",bubbles:true}));
    var last=state.picks[state.picks.length-1];
    if(!last || last.playerId!==target) throw new Error("key 2 drafted the wrong player");
  });

  step("shortcuts-inert-while-typing-elsewhere",function(){
    ensureLeagueOnly("espn10");
    state.sim=false; state.picks=[];
    var box=document.getElementById("syncIn");
    box.focus();
    var before=state.picks.length;
    document.dispatchEvent(new KeyboardEvent("keydown",{key:"1",bubbles:true}));
    document.dispatchEvent(new KeyboardEvent("keydown",{key:"u",bubbles:true}));
    if(state.picks.length!==before) throw new Error("shortcuts fired while typing in another field");
    box.blur();
  });


  step("setup-link-configures-the-device",function(){
    setDraftId("sleeper12",""); setDraftWhen("sleeper12","");
    setDraftWhen("espn10","");
    var fakeId="1111111111111111111";   // never the real id: the privacy scan reads this file too
    var payload={sleeper12:{id:fakeId,when:"2026-08-28T18:30"},
                 espn10:{when:"2026-08-28T19:30"}};
    var res=applySetupHash("#setup="+encodeURIComponent(JSON.stringify(payload)));
    if(!res || res.error) throw new Error("setup rejected: "+(res&&res.error));
    if(draftIdFor("sleeper12")!==fakeId) throw new Error("id not saved");
    if(draftWhenFor("sleeper12")!=="2026-08-28T18:30") throw new Error("sleeper date not saved");
    if(draftWhenFor("espn10")!=="2026-08-28T19:30") throw new Error("espn date not saved");
    if(res.applied.length!==2) throw new Error("expected 2 leagues, got "+res.applied.length);
  });

  step("setup-link-does-not-disturb-draft-import",function(){
    if(applySetupHash("")!==null) throw new Error("empty hash should return null");
    ensureLeagueOnly("espn10");
    var names=available().slice(0,2).map(function(p){return p.name;});
    var draftHash="#draft=espn10:"+encodeURIComponent(names.join("|"));
    if(applySetupHash(draftHash)!==null) throw new Error("setup handler grabbed a draft hash");
    location.hash=draftHash;
    var r=importFromHash();
    location.hash="";
    if(!r || r.count!==2) throw new Error("draft import broken by setup handler");
  });

  /* Note: the payload below splits "</scr"+"ipt>" - a literal closing tag inside an
     injected <script> block ends the block early and kills the whole harness. */
  step("setup-link-rejects-junk",function(){
    var before=draftIdFor("sleeper12");
    var bad=[
      "#setup=not-json",
      "#setup="+encodeURIComponent(JSON.stringify({sleeper12:{id:"<scr"+"ipt>alert(1)</scr"+"ipt>"}})),
      "#setup="+encodeURIComponent(JSON.stringify({sleeper12:{when:"tomorrow"}})),
      "#setup="+encodeURIComponent(JSON.stringify({notALeague:{id:"123"}})),
      "#setup="+encodeURIComponent(JSON.stringify(["array","not","object"]))
    ];
    bad.forEach(function(h){
      var r=applySetupHash(h);
      if(r && !r.error && r.applied && r.applied.length)
        throw new Error("accepted bad payload: "+h.slice(0,45));
    });
    if(draftIdFor("sleeper12")!==before) throw new Error("junk payload mutated saved settings");
  });


  step("cbs-game-bonus-is-calibrated",function(){
    /* Measured from 2025: the ladder pays quarterbacks ~2.9 pts/game and tight ends
       ~0.2. The model must reproduce that shape, and must not touch other leagues. */
    if(Math.abs(bonusPerGame("QB",237)-2.75)>0.01) throw new Error("QB anchor off");
    if(Math.abs(bonusPerGame("TE",60)-0.29)>0.01) throw new Error("TE anchor off");
    if(bonusPerGame("QB",300) <= bonusPerGame("QB",262)) throw new Error("curve must keep rising");
    if(bonusPerGame("QB",0)!==0) throw new Error("zero yards should pay zero");
    if(bonusPerGame("XX",200)!==0) throw new Error("unknown position should pay zero");
    /* Compare each position at yardage it actually produces, not at a shared number
       no receiver has ever posted. */
    if(!(bonusPerGame("QB",250) > bonusPerGame("WR",90)*2))
      throw new Error("the ladder should favour quarterbacks heavily");
    // and extrapolation must stay bounded well outside the measured range
    if(bonusPerGame("WR",400) > 2.3) throw new Error("receiver curve runs away: "+bonusPerGame("WR",400));
    if(bonusPerGame("QB",900) > 6.1) throw new Error("QB curve runs away");
    if(bonusPerGame("TE",500) > 1.3) throw new Error("TE curve runs away");

    ensureLeagueOnly("espn10");
    var allenEspn=PLAYERS.find(function(p){return p.name==="Josh Allen"}).proj;
    ensureLeagueOnly("cbs12");
    var allenCbs=PLAYERS.find(function(p){return p.name==="Josh Allen"}).proj;
    var mcbCbs=PLAYERS.find(function(p){return p.name==="Trey McBride"});
    ensureLeagueOnly("espn10");
    var mcbEspn=PLAYERS.find(function(p){return p.name==="Trey McBride"});
    var qbGain=allenCbs-allenEspn;
    var teGain=mcbCbs.proj-mcbEspn.proj;
    if(qbGain < 60) throw new Error("CBS QB gain only "+qbGain.toFixed(0)+" - bonus not applied?");
    if(teGain > 12) throw new Error("tight end gained "+teGain.toFixed(0)+" - bonus far too generous");
    log.push("   (CBS ladder: Allen +"+qbGain.toFixed(0)+" vs ESPN, McBride +"+teGain.toFixed(0)+")");
  });

  step("bonus-does-not-leak-into-other-leagues",function(){
    ["espn10","mfl12","sleeper12"].forEach(function(k){
      if(SCORING[k].gameBonus) throw new Error(k+" should not use the CBS ladder");
    });
  });


  step("mfl-order-parses-from-the-real-export",function(){
    ensureLeagueOnly("mfl12");
    var parsed=parseMflOrder(MFL_FIXTURE);
    if(parsed.error) throw new Error(parsed.error);
    if(parsed.rounds!==12) throw new Error("expected 12 rounds, got "+parsed.rounds);
    if(parsed.filled!==144) throw new Error("expected 144 slots, got "+parsed.filled);
    setDraftOrder(parsed.order);
    // round 1 from the real export
    var r1=state.order.slice(0,12).map(function(x){return x+1;});
    if(r1.join()!=="12,8,6,2,9,4,5,1,11,7,10,3") throw new Error("round 1 wrong: "+r1.join());
    // round 2 must be its mirror, round 3 must NOT be
    var r2=state.order.slice(12,24).map(function(x){return x+1;});
    var r3=state.order.slice(24,36).map(function(x){return x+1;});
    if(r2.join()!==r1.slice().reverse().join()) throw new Error("round 2 should mirror round 1");
    if(r3.join()===r1.join()||r3.join()===r2.slice().reverse().join())
      throw new Error("round 3 should NOT follow the snake");
    if(describeOrder().indexOf("do not follow the snake")<0)
      throw new Error("app should say the order breaks the snake");
    log.push("   (MFL: "+parsed.rounds+" rounds parsed, round 3 confirmed non-snake)");
  });

  step("clock-follows-the-loaded-order",function(){
    ensureLeagueOnly("mfl12");
    setDraftOrder(parseMflOrder(MFL_FIXTURE).order);
    if(teamOnClock(0)!==11) throw new Error("pick 1 should be franchise 12 (index 11)");
    if(teamOnClock(24)!==2)  throw new Error("round 3 pick 1 should be franchise 3 (index 2)");
    if(teamOnClock(25)!==7)  throw new Error("round 3 pick 2 should be franchise 8 (index 7)");
    // and picks recorded under it get the right owner
    state.sim=false; state.picks=[];
    makePick(PLAYERS[0].id); makePick(PLAYERS[1].id);
    if(state.picks[0].team!==11||state.picks[1].team!==7)
      throw new Error("picks not attributed to the loaded order");
  });

  step("loading-an-order-reattributes-existing-picks",function(){
    ensureLeagueOnly("mfl12");
    setDraftOrder(null);
    state.sim=false; state.picks=[];
    makePick(PLAYERS[0].id); makePick(PLAYERS[1].id); makePick(PLAYERS[2].id);
    var snakeTeams=state.picks.map(function(pk){return pk.team;}).join();
    setDraftOrder(parseMflOrder(MFL_FIXTURE).order);
    var newTeams=state.picks.map(function(pk){return pk.team;}).join();
    if(snakeTeams===newTeams) throw new Error("existing picks were not re-attributed");
    state.picks.forEach(function(pk,i){
      if(pk.team!==teamOnClock(i)) throw new Error("pick "+i+" disagrees with the order");
    });
  });

  step("order-survives-a-league-switch",function(){
    ensureLeagueOnly("mfl12");
    setDraftOrder(parseMflOrder(MFL_FIXTURE).order);
    var first=teamOnClock(24);
    applyLeague("espn10");
    if(state.order!==null) throw new Error("espn should be back on a snake");
    if(teamOnClock(0)!==0) throw new Error("espn snake broken");
    applyLeague("mfl12");
    if(!state.order) throw new Error("mfl order not restored");
    if(teamOnClock(24)!==first) throw new Error("restored order differs");
  });

  step("one-round-order-repeats",function(){
    ensureLeagueOnly("mfl12");
    setDraftOrder(null);
    var r=loadOrderFromText("3,8,5,12,9,10,6,7,2,4,11,1");
    if(r.error) throw new Error(r.error);
    if(teamOnClock(0)!==2) throw new Error("first pick wrong");
    if(teamOnClock(12)!==2) throw new Error("order should repeat, not snake");
    var bad=loadOrderFromText("1,2,3");
    if(!bad.error) throw new Error("short order should be rejected");
    var bad2=loadOrderFromText("1,2,3,4,5,6,7,8,9,10,11,99");
    if(!bad2.error) throw new Error("out-of-range team should be rejected");
    var bad3=loadOrderFromText("{\"nonsense\":true}");
    if(!bad3.error) throw new Error("bad JSON should be rejected");
    setDraftOrder(null);
  });


  step("mocks-save-load-and-grade",function(){
    try{ localStorage.removeItem("warroom.mocks.v1"); }catch(e){}
    ensureDraft("espn10", 3);
    var roster=rosterOf(myIdx()).map(function(p){return p.name;}).join();
    var r=saveMock("seat 3 test");
    if(r.error) throw new Error(r.error);
    if(!(r.grade.points>0)) throw new Error("grade has no points");
    if(r.grade.rank<1||r.grade.rank>state.teams) throw new Error("rank out of range");

    // a different seat should produce a different roster, and both are kept
    ensureDraft("espn10", 9);
    saveMock("seat 9 test");
    var mine=loadMocks().filter(function(m){return m.league==="espn10";});
    if(mine.length!==2) throw new Error("expected 2 saves, got "+mine.length);

    // load the first back and confirm the roster is restored exactly
    var target=mine.filter(function(m){return m.name==="seat 3 test";})[0];
    var lr=loadMock(target.id);
    if(lr.error) throw new Error(lr.error);
    if(state.slot!==3) throw new Error("seat not restored");
    if(rosterOf(myIdx()).map(function(p){return p.name;}).join()!==roster)
      throw new Error("roster not restored");
    log.push("   (mocks: seat 3 "+target.grade.points.toFixed(0)+" pts rank "+target.grade.rank+")");
  });

  step("mocks-are-scoped-per-league",function(){
    try{ localStorage.removeItem("warroom.mocks.v1"); }catch(e){}
    ensureDraft("espn10", 1); saveMock("espn one");
    ensureDraft("cbs12", 1);  saveMock("cbs one");
    renderDraft();
    var shown=document.getElementById("mocksOut").textContent;
    if(shown.indexOf("cbs one")<0) throw new Error("cbs save not listed while in cbs");
    if(shown.indexOf("espn one")>=0) throw new Error("espn save leaked into the cbs list");
    if(loadMocks().length!==2) throw new Error("both should still be stored");
  });

  step("mocks-restore-a-custom-order",function(){
    try{ localStorage.removeItem("warroom.mocks.v1"); }catch(e){}
    ensureLeagueOnly("mfl12");
    setDraftOrder(parseMflOrder(MFL_FIXTURE).order);
    state.sim=false; state.picks=[];
    makePick(PLAYERS[0].id); makePick(PLAYERS[1].id);
    saveMock("with order");
    setDraftOrder(null);
    if(state.order) throw new Error("order should be cleared");
    var m=loadMocks()[0];
    loadMock(m.id);
    if(!state.order) throw new Error("order not restored with the mock");
    if(teamOnClock(24)!==2) throw new Error("restored order is wrong");
    setDraftOrder(null);
  });

  step("mocks-handle-an-empty-draft-and-bad-id",function(){
    ensureLeagueOnly("espn10");
    state.picks=[];
    if(!saveMock("nothing").error) throw new Error("saving an empty draft should be refused");
    if(!loadMock("does-not-exist").error) throw new Error("unknown id should error");
  });


  step("defence-names-resolve-from-every-host",function(){
    ensureLeagueOnly("espn10");
    var forms=["Buffalo Defense","Buffalo Bills","Bills, Buffalo","Bills","Buffalo",
               "BUF Defense","Bills D/ST","buffalo dst"];
    forms.forEach(function(f){
      var norm=f.indexOf(",")>=0 ? f.split(", ")[1]+" "+f.split(", ")[0] : f;
      var hit=NORM.get(normName(norm.replace("D/ST","dst")));
      if(!hit) throw new Error("no match for '"+f+"'");
      if(hit.pos!=="DEF"||hit.team!=="BUF") throw new Error("'"+f+"' matched "+hit.name);
    });
    // and a two-word city still works
    ["Kansas City Chiefs","Chiefs","Kansas City"].forEach(function(f){
      var hit=NORM.get(normName(f));
      if(!hit||hit.team!=="KC") throw new Error("KC form failed: "+f);
    });
    log.push("   (defence aliases: "+forms.length+" naming styles all resolve)");
  });

  step("mfl-hash-loads-order-and-picks",function(){
    ensureLeagueOnly("mfl12");
    setDraftOrder(null); state.picks=[];
    var parsed=parseMflOrder(MFL_FIXTURE);
    var names=available().slice(0,4).map(function(p){return p.name;});
    var payload={league:"mfl12",order:parsed.order,names:names};
    var r=applyMflHash("#mfl="+encodeURIComponent(JSON.stringify(payload)));
    if(!r||r.error) throw new Error("mfl sync failed: "+(r&&r.error));
    if(!state.order) throw new Error("order not applied");
    if(state.picks.length!==4) throw new Error("picks not applied: "+state.picks.length);
    if(teamOnClock(24)!==2) throw new Error("order wrong after sync");
    if(state.picks[0].team!==11) throw new Error("first pick owner wrong");
    if(applyMflHash("#something-else")!==null) throw new Error("should ignore other hashes");
    if(!applyMflHash("#mfl=nonsense").error) throw new Error("bad payload should error");
    var bad=applyMflHash("#mfl="+encodeURIComponent(JSON.stringify({league:"mfl12",order:[0,1,99]})));
    if(!bad.error) throw new Error("out-of-range team should be rejected");
    setDraftOrder(null); state.picks=[];
  });


  step("adp-sources-blend-and-switch",function(){
    ensureLeagueOnly("espn10");
    var t=PLAYERS.find(function(p){return p.pos==="WR"});
    var boardAdp=t.adpBoard!==undefined?t.adpBoard:t.adp;
    // stand in for the live market with a deliberately different price
    LIVEDATA=liveRowsToMaps([{name:t.name,pos:t.pos,team:t.team,gp:18,passYd:0,passTd:0,int:0,
      rushYd:0,rushTd:0,rec:80,recYd:1000,recTd:6,fum:0,sleeperPts:120,
      adpStd:boardAdp+40, adpPpr:boardAdp+40, adp2qb:boardAdp+40, inj:""}], Date.now());

    state.adpSource="board"; applyLeague("espn10");
    var a=PLAYERS.find(function(p){return p.name===t.name;});
    if(Math.abs(a.adp-boardAdp)>0.01) throw new Error("board mode should use the board price");

    state.adpSource="sleeper"; applyLeague("espn10");
    var b=PLAYERS.find(function(p){return p.name===t.name;});
    if(Math.abs(b.adp-(boardAdp+40))>0.01) throw new Error("sleeper mode should use the live price");

    state.adpSource="blend"; applyLeague("espn10");
    var c=PLAYERS.find(function(p){return p.name===t.name;});
    if(Math.abs(c.adp-(boardAdp+20))>0.01)
      throw new Error("blend should average the two: expected "+(boardAdp+20)+", got "+c.adp);
    if(adpGapNote(c).indexOf("falls")<0) throw new Error("a 40-pick gap should be flagged");

    // a player only one source knows about must not be dropped or NaN'd
    var solo=PLAYERS.find(function(p){return p.adpLive===null;});
    if(solo && !isFinite(solo.adp)) throw new Error("single-source player lost its price");

    LIVEDATA=null; state.adpSource="blend"; applyLeague("espn10");
    var d=PLAYERS.find(function(p){return p.name===t.name;});
    if(Math.abs(d.adp-boardAdp)>0.01) throw new Error("with no live data it must fall back to the board");
    log.push("   (ADP blend: board "+boardAdp.toFixed(0)+", live "+(boardAdp+40).toFixed(0)+", blended "+(boardAdp+20).toFixed(0)+")");
  });


  step("proj-hash-rejects-junk",function(){
    ensureLeagueOnly("espn10");
    if(applyProjHash("#draft=espn10:x")!==null) throw new Error("grabbed a draft hash");
    if(!applyProjHash("#proj=notjson").error) throw new Error("bad JSON accepted");
    if(!applyProjHash("#proj="+encodeURIComponent(JSON.stringify({rows:[]}))).error)
      throw new Error("empty rows accepted");
    if(!applyProjHash("#proj="+encodeURIComponent(JSON.stringify({rows:[{bad:1}]}))).error)
      throw new Error("malformed rows accepted");
    FPDATA=null; applyLeague("espn10");
  });

  step("fp-bookmarklet-is-built",function(){
    ensureLeagueOnly("espn10");
    var v=document.getElementById("fpCode").value;
    if(v.indexOf("fantasypros")>=0 && v.indexOf("/nfl/projections/")<0)
      throw new Error("bookmarklet does not read the projections pages");
    ["qb","rb","wr","te"].forEach(function(p){
      if(v.indexOf("'"+p+"'")<0) throw new Error("missing position "+p);
    });
    if(v.indexOf("#proj=")<0) throw new Error("does not hand data back");
    if(v.indexOf("XMLHttpRequest")<0) throw new Error("should use a same-origin request");
  });


  step("multiple-projection-sources-average",function(){
    ensureLeagueOnly("espn10");
    EXTRA_PROJ={}; applyLeague("espn10");
    var t=PLAYERS.find(function(p){return p.pos==="RB" && p.proj!==null;});
    var solo=t.proj;

    // two outside sources, one bullish one bearish
    applyProjHash("#proj="+encodeURIComponent(JSON.stringify(
      {src:"fp", rows:[{n:t.name,p:"RB",ry:2000,rt:20,rc:80,cy:800,ct:5,f:1}]})));
    applyProjHash("#proj="+encodeURIComponent(JSON.stringify(
      {src:"fbg",rows:[{n:t.name,p:"RB",ry:400,rt:2,rc:10,cy:80,ct:0,f:1}]})));
    var a=PLAYERS.find(function(x){return x.name===t.name;});
    if(Object.keys(a.projBySrc).length!==2) throw new Error("expected 2 outside sources");
    var mean=(a.projSleeper+a.projBySrc.fp+a.projBySrc.fbg)/3;
    if(Math.abs(a.proj-Math.round(mean*10)/10)>0.2)
      throw new Error("blend should be the mean of 3: "+a.proj+" vs "+mean.toFixed(1));
    if(!(a.projSpread>0)) throw new Error("spread should be positive when sources differ");

    state.projSource="fbg"; applyLeague("espn10");
    var b=PLAYERS.find(function(x){return x.name===t.name;});
    if(Math.abs(b.proj-b.projBySrc.fbg)>0.2) throw new Error("fbg-only mode wrong");

    state.projSource="blend"; EXTRA_PROJ={}; applyLeague("espn10");
    var c=PLAYERS.find(function(x){return x.name===t.name;});
    if(Math.abs(c.proj-solo)>0.2) throw new Error("should fall back to Sleeper alone");
    if(c.projSpread!==0) throw new Error("single source should have no spread");
    log.push("   (3-source blend verified, spread reported)");
  });

  step("re-importing-one-source-keeps-the-other",function(){
    ensureLeagueOnly("espn10");
    EXTRA_PROJ={};
    var a=PLAYERS[0], b=PLAYERS[1];
    applyProjHash("#proj="+encodeURIComponent(JSON.stringify(
      {src:"fp", rows:[{n:a.name,p:a.pos,ry:500,rt:3,rc:20,cy:200,ct:1,f:0}]})));
    applyProjHash("#proj="+encodeURIComponent(JSON.stringify(
      {src:"fbg",rows:[{n:b.name,p:b.pos,ry:400,rt:2,rc:10,cy:100,ct:1,f:0}]})));
    if(sourcesLoaded().length!==2) throw new Error("both sources should be held");
    // a second fbg batch for a different player must ADD, not replace
    applyProjHash("#proj="+encodeURIComponent(JSON.stringify(
      {src:"fbg",rows:[{n:a.name,p:a.pos,ry:450,rt:2,rc:12,cy:120,ct:1,f:0}]})));
    if(EXTRA_PROJ.fbg.count!==2) throw new Error("fbg batches should merge, got "+EXTRA_PROJ.fbg.count);
    if(EXTRA_PROJ.fp.count!==1) throw new Error("fp source was disturbed");
    EXTRA_PROJ={}; applyLeague("espn10");
  });

  step("fbg-bookmarklet-reads-headers-not-fixed-indices",function(){
    ensureLeagueOnly("espn10");
    var v=document.getElementById("fbgCode").value;
    if(v.indexOf("projections_table")<0) throw new Error("does not target their table");
    if(v.indexOf("thead")<0) throw new Error("should read the header row rather than assume columns");
    if(v.indexOf("src:'fbg'")<0) throw new Error("payload not tagged as footballguys");
    var fp=document.getElementById("fpCode").value;
    if(fp.indexOf("src:'fp'")<0) throw new Error("fantasypros payload not tagged");
  });


  step("fbg-urls-carry-each-league-scoring",function(){
    var u=fbgUrl("cbs12","qb");
    if(u.indexOf("pass-td=6")<0) throw new Error("CBS should request 6-point passing TDs");
    if(u.indexOf("ppr=0")<0) throw new Error("CBS is not PPR");
    if(u.indexOf("numTeams=12")<0) throw new Error("CBS team count wrong");
    var e=fbgUrl("espn10","rb");
    if(e.indexOf("pass-td=4")<0||e.indexOf("numTeams=10")<0) throw new Error("ESPN settings wrong");
    if(e.indexOf("ppr=0")<0) throw new Error("ESPN is not PPR");
    var s=fbgUrl("sleeper12","wr");
    if(s.indexOf("ppr=1")<0) throw new Error("Sleeper is full PPR");
    if(s.indexOf("wr=3")<0) throw new Error("Sleeper starts three receivers");
    if(s.indexOf(encodeURIComponent("qb,rb,wr,te")+"=1")<0)
      throw new Error("Sleeper superflex slot not requested");
    var m=fbgUrl("mfl12","te");
    if(m.indexOf("ppr=1")<0||m.indexOf("pass-td=6")<0) throw new Error("MFL settings wrong");
    ["qb","rb","wr","te"].forEach(function(pos){
      if(fbgUrl("espn10",pos).indexOf("pos="+pos)<0) throw new Error("position missing for "+pos);
    });
  });

  step("scoring-audit-compares-like-for-like",function(){
    ensureLeagueOnly("cbs12");
    EXTRA_PROJ={};
    if(scoringAudit()!==null) throw new Error("audit should be null with no fbg data");
    /* Josh Allen exactly as Footballguys projects him, with their own CBS-configured
       total. Our engine should land within a couple of percent. */
    applyProjHash("#proj="+encodeURIComponent(JSON.stringify({src:"fbg", rows:[
      {n:"Josh Allen",p:"QB",py:3770,pt:27.2,i:10.8,ry:553,rt:11.2,rc:0,cy:0,ct:0,f:0,tp:411.53}
    ]})));
    var a=scoringAudit();
    if(!a) throw new Error("audit produced nothing");
    if(a.n!==1) throw new Error("expected one comparable player");
    if(a.medianPct>4)
      throw new Error("our CBS scoring is "+a.medianPct+"% from theirs - check the rules");
    /* interceptions are a positive count; the multiplier carries the penalty. If the
       sign were doubled up this player would score ~43 points too high. */
    var ip=scoreRow({passYd:0,passTd:0,int:10,rushYd:0,rushTd:0,rec:0,recYd:0,recTd:0,fum:0,gp:17,sleeperPts:0},
                    SCORING.cbs12,"QB");
    if(ip>0) throw new Error("ten interceptions should not be worth positive points");
    renderAudit();
    if(document.getElementById("auditOut").textContent.indexOf("median difference")<0)
      throw new Error("audit panel did not render");
    log.push("   (scoring audit vs Footballguys CBS: "+a.medianPct.toFixed(1)+"% apart)");
    EXTRA_PROJ={}; applyLeague("espn10");
  });

  step("audit-catches-a-wrong-rule",function(){
    ensureLeagueOnly("cbs12");
    EXTRA_PROJ={};
    // same player, but a total that implies 4-point passing TDs instead of 6
    applyProjHash("#proj="+encodeURIComponent(JSON.stringify({src:"fbg", rows:[
      {n:"Josh Allen",p:"QB",py:3770,pt:27.2,i:10.8,ry:553,rt:11.2,rc:0,cy:0,ct:0,f:0,tp:250}
    ]})));
    var a=scoringAudit();
    if(!a || a.medianPct < 10)
      throw new Error("a badly wrong total should show a large gap, got "+(a&&a.medianPct));
    EXTRA_PROJ={}; applyLeague("espn10");
  });


  step("real-depth-charts-loaded",function(){
    ensureLeagueOnly("espn10");
    var teams=Object.keys(DEPTH.byTeamPos).map(function(k){return k.split("|")[0];});
    if(new Set(teams).size!==32) throw new Error("expected 32 teams, got "+new Set(teams).size);
    ["QB","RB","WR","TE"].forEach(function(pos){
      var det=DEPTH.byTeamPos["DET|"+pos];
      if(!det||!det.length) throw new Error("no Detroit "+pos+" depth");
      if(det[0].rank!==1) throw new Error(pos+" list should start at 1");
    });
    var goff=DEPTH.byName.get(normName("Jared Goff")+"|QB");
    if(!goff||goff.rank!==1||goff.team!=="DET") throw new Error("Goff should be Detroit QB1");
    var arsb=DEPTH.byName.get(normName("Amon-Ra St. Brown")+"|WR");
    if(!arsb||arsb.rank!==1) throw new Error("St. Brown should be Detroit WR1");
    if(arsb.slot!=="slot") throw new Error("alignment lost, got "+arsb.slot);
  });

  step("depth-vs-market-disagreement",function(){
    ensureLeagueOnly("espn10");
    var withBoth=PLAYERS.filter(function(p){return p.depthRank!==null && p.marketRank;});
    if(withBoth.length<80) throw new Error("only "+withBoth.length+" players have both rankings");
    // market rank must be a dense 1..n per team+position
    var seen={};
    PLAYERS.slice().sort(function(a,b){return a.adp-b.adp;}).forEach(function(p){
      var k=p.team+"|"+p.pos; seen[k]=(seen[k]||0)+1;
      if(p.marketRank!==seen[k]) throw new Error("market rank not sequential for "+k);
    });
    var gaps=withBoth.filter(function(p){return Math.abs(p.depthGap)>=1;});
    if(!gaps.length) throw new Error("no disagreements at all - suspicious");
    var badged=gaps.filter(function(p){return depthNote(p)!=="";});
    if(badged.length!==gaps.length) throw new Error("some disagreements are not badged");
    if(depthNote(withBoth.filter(function(p){return p.depthGap===0;})[0]||{depthGap:0})!=="")
      throw new Error("agreement should not be badged");
    log.push("   (depth charts: "+withBoth.length+" players ranked by both, "+gaps.length+" disagree)");
  });

  step("depth-tab-leads-with-the-team",function(){
    ensureLeagueOnly("espn10");
    state.tab="depth"; document.getElementById("p-depth").hidden=false;
    renderDepth();
    var html=document.getElementById("depthOut").innerHTML;
    if(html.indexOf("Jared Goff")<0) throw new Error("depth tab missing a listed starter");
    if(html.indexOf("mkt ")<0) throw new Error("no market-disagreement markers rendered");
  });

  // ---- importer ----
  step("import-sleeper-json",function(){
    applyLeague("sleeper12"); state.picks=[]; state.sim=false;
    var fake=[
      {pick_no:2, metadata:{first_name:"Jahmyr", last_name:"Gibbs"}},
      {pick_no:1, metadata:{first_name:"Josh",   last_name:"Allen"}},
      {pick_no:3, metadata:{first_name:"Bijan",  last_name:"Robinson"}}
    ];
    document.getElementById("syncIn").value=JSON.stringify(fake);
    document.getElementById("syncGo").click();
    if(state.picks.length!==3) throw new Error("imported "+state.picks.length);
    var first=byId.get(state.picks[0].playerId).name;
    if(first!=="Josh Allen") throw new Error("pick order wrong, got "+first);
    if(state.sim!==false) throw new Error("sim should be off after import");
  });

  step("import-name-list-and-suffixes",function(){
    applyLeague("espn10"); state.picks=[];
    document.getElementById("syncIn").value=
      "Jahmyr Gibbs\nBijan Robinson\nA.J. Brown\nJames Cook III\nMarvin Harrison Jr.";
    document.getElementById("syncGo").click();
    if(state.picks.length!==5) throw new Error("imported "+state.picks.length+" of 5");
  });

  step("import-reports-unmatched",function(){
    /* An unmatched name is still reported, but no longer vanishes: it holds its slot
       so every pick after it keeps its true number. */
    applyLeague("espn10"); state.picks=[];
    document.getElementById("syncIn").value="Bijan Robinson" + String.fromCharCode(10) + "Not A Real Person";
    document.getElementById("syncGo").click();
    if(state.picks.length!==2)
      throw new Error("2 picks happened, recorded "+state.picks.length);
    var second=byId.get(state.picks[1].playerId);
    if(!second || !second.offBoard) throw new Error("second pick is not a placeholder");
    if(document.getElementById("syncMsg").textContent.indexOf("Not matched")<0)
      throw new Error("no unmatched warning");
    clearPlaceholders();
  });

  step("import-rejects-garbage",function(){
    applyLeague("espn10"); state.picks=[];
    document.getElementById("syncIn").value="{not json at all";
    document.getElementById("syncGo").click();
    if(document.getElementById("syncMsg").textContent.indexOf("valid JSON")<0)
      throw new Error("no JSON error shown");
  });

  step("hash-sync-loads-picks",function(){
    applyLeague("espn10"); state.picks=[];
    location.hash = "#draft=sleeper12:" + encodeURIComponent("Josh Allen|Jahmyr Gibbs|Bijan Robinson");
    var res = importFromHash();
    if(!res) throw new Error("hash not recognised");
    if(state.league!=="sleeper12") throw new Error("league not switched, got "+state.league);
    if(res.count!==3) throw new Error("imported "+res.count);
    if(byId.get(state.picks[0].playerId).name!=="Josh Allen") throw new Error("wrong order");
    if(state.sim!==false) throw new Error("sim still on");
  });

  step("hash-resync-does-not-double-count",function(){
    var res = importFromHash();          // same hash again, as a re-click would
    if(res.count!==3) throw new Error("re-sync produced "+res.count);
  });

  step("hash-ignores-junk",function(){
    location.hash = "#draft=notaleague:Whoever";
    if(importFromHash()!==null) throw new Error("accepted unknown league");
    location.hash = "#somethingelse";
    if(importFromHash()!==null) throw new Error("accepted unrelated hash");
    location.hash = "";
  });

  step("superflex-drafts-two-QBs",function(){
    applyLeague("sleeper12");
    var withTwo=0;
    for(var sl=1; sl<=12; sl+=4){
      state.slot=sl; state.sim=true; state.picks=[]; reseed(); playOut();
      if(counts(sl-1).QB>=2) withTwo++;
    }
    if(withTwo<3) throw new Error("only "+withTwo+"/3 slots got two QBs");
  });

  /* ---- live sync ----
     The Live sync box shipped once with no listener behind it: it ticked, looked on,
     and the board never moved. These assert the wiring exists and behaves, because a
     silently dead switch during a live draft is the worst failure this app has. */
  step("live-sync-switch-is-wired",function(){
    if(typeof liveSyncStart !== "function") throw new Error("no liveSyncStart");
    if(typeof liveSyncTick  !== "function") throw new Error("no liveSyncTick");
    if(typeof liveSyncStop  !== "function") throw new Error("no liveSyncStop");
    var box=document.getElementById("liveOn");
    if(!box) throw new Error("no liveOn checkbox");
    /* Prove the handler is attached by firing the event and watching for an effect. */
    window.LIVE_CAPABLE=true;
    setDraftId("sleeper12","");
    applyLeague("sleeper12");
    box.checked=true;
    box.dispatchEvent(new Event("change"));
    if(box.checked) throw new Error("no draft id, yet the switch stayed on");
  });

  step("live-sync-refuses-without-a-draft-id",function(){
    setDraftId("sleeper12","");
    applyLeague("sleeper12");
    liveSyncStart();
    if(state.liveOn) throw new Error("started with no draft id");
    var m=document.getElementById("liveMsg");
    if(!m || m.textContent.indexOf("draft ID")<0) throw new Error("no useful message");
  });

  await astep("live-sync-applies-picks-from-the-feed",async function(){
    setDraftId("sleeper12","999");
    applyLeague("sleeper12");
    state.picks=[]; state.sim=false;
    var top=PLAYERS.slice().sort(function(a,b){return a.adp-b.adp;}).slice(0,5);
    var real=window.fetch;
    window.fetch=function(){ return Promise.resolve({ok:true, status:200, json:function(){
      return Promise.resolve(top.map(function(p,i){
        var c=p.name.split(" ");
        return {pick_no:i+1, metadata:{first_name:c[0], last_name:c.slice(1).join(" ")}};
      }));
    }}); };
    LIVE_SYNC={timer:null,key:"sleeper12",last:-1,fails:0,at:0};
    try{ await liveSyncTick(); } finally { window.fetch=real; }
    if(state.picks.length!==5) throw new Error("applied "+state.picks.length+" of 5");
  });

  await astep("live-sync-ignores-a-quiet-feed",async function(){
    /* When the pick count has not moved there is nothing to do, and re-applying would
       rebuild the whole board fifteen seconds apart for no reason. Spy on the apply
       path rather than the outcome: an unchanged board looks identical either way, so
       only the absence of the work proves the skip is real. */
    setDraftId("sleeper12","999");
    applyLeague("sleeper12");
    state.picks=[]; state.sim=false;
    var top=PLAYERS.slice().sort(function(a,b){return a.adp-b.adp;}).slice(0,3);
    var feed=top.map(function(p,i){
      var c=p.name.split(" ");
      return {pick_no:i+1, metadata:{first_name:c[0], last_name:c.slice(1).join(" ")}};
    });
    var real=window.fetch, calls=0;
    window.fetch=function(){ calls++; return Promise.resolve({ok:true,status:200,
      json:function(){ return Promise.resolve(feed); }}); };
    var realApply=window.applyNames, applies=0;
    window.applyNames=function(n){ applies++; return realApply(n); };
    LIVE_SYNC={timer:null,key:"sleeper12",last:-1,fails:0,at:0};
    try{
      await liveSyncTick();          // first read: three new picks, should apply
      if(applies!==1) throw new Error("first read applied "+applies+" times");
      if(state.picks.length!==3) throw new Error("first read gave "+state.picks.length+" picks");
      await liveSyncTick();          // same three: should do nothing
      if(applies!==1) throw new Error("re-applied an unchanged feed");
      if(state.picks.length!==3) throw new Error("quiet tick disturbed the board");
    } finally { window.fetch=real; window.applyNames=realApply; }
    if(calls!==2) throw new Error("expected two requests, got "+calls);
  });

  await astep("live-sync-gives-up-after-repeated-failures",async function(){
    var real=window.fetch;
    window.fetch=function(){ return Promise.reject(new Error("offline")); };
    setDraftId("sleeper12","999");
    LIVE_SYNC={timer:null,key:"sleeper12",last:-1,fails:0,at:0};
    state.liveOn=true;
    try{
      for(var i=0;i<5;i++) await liveSyncTick();
    } finally { window.fetch=real; }
    if(state.liveOn) throw new Error("kept trying forever");
  });

  await astep("empty-feed-does-not-wipe-a-hand-entered-board",async function(){
    /* Before a draft opens, Sleeper answers with an empty array. Feeding that to
       applyNames would clear picks someone typed in while waiting - which is exactly
       when they would be typing them in. */
    setDraftId("sleeper12","999");
    applyLeague("sleeper12");
    state.picks=[]; state.sim=false;
    var top=PLAYERS.slice().sort(function(a,b){return a.adp-b.adp;}).slice(0,4);
    applyNames(top.map(function(p){ return p.name; }));
    if(state.picks.length!==4) throw new Error("setup failed: "+state.picks.length+" picks");
    var real=window.fetch;
    window.fetch=function(){ return Promise.resolve({ok:true,status:200,
      json:function(){ return Promise.resolve([]); }}); };
    LIVE_SYNC={timer:null,key:"sleeper12",last:-1,fails:0,at:0};
    try{ await liveSyncTick(); } finally { window.fetch=real; }
    if(state.picks.length!==4)
      throw new Error("empty feed wiped the board: "+state.picks.length+" picks left");
    var m=document.getElementById("liveMsg");
    if(!m || m.textContent.indexOf("not started")<0)
      throw new Error("no explanation shown");
  });

  await astep("two-drafts-the-same-night-do-not-contaminate-each-other",async function(){
    /* Sleeper opens 6:30 and ESPN 7:30 on the 28th, so both boards are live at once and
       he will be switching between them every few minutes. An earlier build wiped picks
       on every switch. This asserts the whole round trip: draft A, switch, draft B,
       switch back, with a poller running against A the entire time. */
    setDraftId("sleeper12","999");
    applyLeague("sleeper12");
    state.picks=[]; state.sim=false;
    var byAdp=PLAYERS.slice().sort(function(a,b){return a.adp-b.adp;});
    var feed=byAdp.slice(0,6).map(function(p,i){
      var c=p.name.split(" ");
      return {pick_no:i+1, metadata:{first_name:c[0], last_name:c.slice(1).join(" ")}};
    });
    var real=window.fetch;
    window.fetch=function(){ return Promise.resolve({ok:true,status:200,
      json:function(){ return Promise.resolve(feed); }}); };
    LIVE_SYNC={timer:null,key:"sleeper12",last:-1,fails:0,at:0};
    try{ await liveSyncTick(); } finally { window.fetch=real; }
    var sleeperPicks=state.picks.length;
    var sleeperNames=state.picks.map(function(pk){ return byId.get(pk.playerId).name; }).join("|");
    if(sleeperPicks!==6) throw new Error("sleeper board has "+sleeperPicks+" of 6");

    /* Over to the offline ESPN draft, entered by hand. */
    applyLeague("espn10");
    if(state.picks.length!==0) throw new Error("espn board opened with sleeper picks on it");
    var espnPick=byAdp.slice(20,24).map(function(p){ return p.name; });
    applyNames(espnPick);
    if(state.picks.length!==4) throw new Error("espn board took "+state.picks.length+" of 4");
    var espnNames=state.picks.map(function(pk){ return byId.get(pk.playerId).name; }).join("|");

    /* Back to Sleeper: its six picks must still be there, unchanged. */
    applyLeague("sleeper12");
    if(state.picks.length!==6)
      throw new Error("sleeper board came back with "+state.picks.length+" picks, not 6");
    if(state.picks.map(function(pk){ return byId.get(pk.playerId).name; }).join("|")!==sleeperNames)
      throw new Error("sleeper board came back with different players");

    /* And ESPN is still intact too. */
    applyLeague("espn10");
    if(state.picks.map(function(pk){ return byId.get(pk.playerId).name; }).join("|")!==espnNames)
      throw new Error("espn board was altered by the round trip");

    /* The poller must not have followed us to ESPN. */
    if(LIVE_SYNC.timer) throw new Error("poller still running on the wrong league");
  });

  step("data-stamp-names-every-loaded-source",function(){
    /* The header claims its own provenance. After a handover it once still read
       "Sleeper only" while a second source was loaded and in the blend - a stamp that
       can be stale is worse than no stamp, because it is believed. */
    EXTRA_PROJ = {};
    applyLeague("sleeper12");
    dataStamp();
    var before = document.getElementById("dataMsg").textContent;
    if(before.indexOf("Sleeper") < 0) throw new Error("stamp never names Sleeper");
    var res = applyProjHash('#proj=' + encodeURIComponent(JSON.stringify({src:"fbg", rows:[
      {n:"Jahmyr Gibbs", p:"RB", py:0,pt:0,i:0, ry:1310, rt:13.1, rc:64.5, cy:534, ct:2.9, f:0}
    ]})));
    if(!res || res.error) throw new Error("handover rejected: " + (res && res.error));
    showProjResult(res);
    var after = document.getElementById("dataMsg").textContent;
    if(after.indexOf("Footballguys") < 0)
      throw new Error("stamp still reads: " + after.slice(0, 90));
    if(sourcesLoaded().indexOf("fbg") < 0) throw new Error("source not registered");
    EXTRA_PROJ = {};
    applyLeague("sleeper12");
  });

  step("an-unmatched-pick-still-holds-its-slot",function(){
    /* Replaying a real completed draft: 168 picks in, 130 matched, and the clock was
       announced from 130. Every pick of a player outside the board shifted the draft
       backwards - the one number you cannot have wrong on the night. */
    applyLeague("sleeper12");
    var top=PLAYERS.slice().sort(function(a,b){return a.adp-b.adp;}).slice(0,5);
    var names=[top[0].name, top[1].name, "Someone Not On This Board",
               top[2].name, "Another Unknown Person", top[3].name];
    var res=applyNames(names);
    if(state.picks.length!==6)
      throw new Error("6 picks happened, board recorded "+state.picks.length);
    if(res.missed.length!==2)
      throw new Error("expected 2 reported unmatched, got "+res.missed.length);
    /* The known players must sit at their true overall positions. */
    if(byId.get(state.picks[3].playerId).name !== top[2].name)
      throw new Error("pick 4 is "+byId.get(state.picks[3].playerId).name+", expected "+top[2].name);
    if(byId.get(state.picks[5].playerId).name !== top[3].name)
      throw new Error("pick 6 landed wrong");
    /* And attribution follows the true slot, not a compressed one. */
    if(state.picks[5].team !== teamOnClock(5))
      throw new Error("pick 6 attributed to the wrong team");
    clearPlaceholders();
  });

  step("repeated-unknown-names-are-separate-picks",function(){
    /* The fuzz soak found this: keying placeholders by name meant the same unknown
       text twice produced one id twice, which reads as a player drafted twice. */
    applyLeague("sleeper12");
    var res=applyNames(["Mystery Man", PLAYERS[0].name, "Mystery Man", "", "  "]);
    if(state.picks.length!==3)
      throw new Error("expected 3 picks (blanks skipped), got "+state.picks.length);
    var ids=state.picks.map(function(pk){ return pk.playerId; });
    if(new Set(ids).size !== ids.length) throw new Error("duplicate pick id");
    if(res.missed.length!==2) throw new Error("expected 2 unmatched, got "+res.missed.length);
    clearPlaceholders();
  });

  step("a-placeholder-on-my-roster-renders-cleanly",function(){
    /* The fuzz soak found renders dying, then printing the literal word "undefined",
       once a placeholder reached My Team. That path is real: he can draft someone
       outside the top-200 board himself and the feed reports it back. */
    applyLeague("sleeper12");
    state.picks=[]; state.sim=false;
    applyNames([PLAYERS[0].name, "Nobody From The Board"]);
    state.picks.forEach(function(pk){ pk.team = myIdx(); });
    var prevTab = state.tab;
    state.tab = "team";
    renderAll();
    var html = document.getElementById("teamOut").innerHTML;
    if(html.indexOf("undefined") >= 0)
      throw new Error("undefined rendered in My Team");
    if(html.indexOf("NaN") >= 0) throw new Error("NaN rendered in My Team");
    if(html.indexOf("[object Object]") >= 0) throw new Error("raw object rendered");
    state.tab = prevTab;
    clearPlaceholders();
  });

  step("placeholders-never-reach-the-board",function(){
    applyLeague("sleeper12");
    applyNames(["Totally Unknown Person", PLAYERS[0].name]);
    var ph=state.picks.filter(function(pk){
      var p=byId.get(pk.playerId); return p && p.offBoard; });
    if(!ph.length) throw new Error("no placeholder was created");
    var id=ph[0].playerId;
    if(PLAYERS.some(function(p){ return p.id===id; }))
      throw new Error("placeholder leaked into PLAYERS");
    if(NORM.get(normName("Totally Unknown Person")))
      throw new Error("placeholder became draftable by name");
    if(recommend().some(function(r){ return r.p.id===id; }))
      throw new Error("placeholder was recommended");
    var lu=bestLineup(rosterOf(myIdx())).slots;
    if(lu.some(function(s){ return s && s.p && s.p.id===id; }))
      throw new Error("placeholder was put in a lineup");
    clearPlaceholders();
  });

  step("placeholders-survive-a-league-switch",function(){
    applyLeague("sleeper12");
    applyNames([PLAYERS[0].name, "Ghost Of Drafts Past", PLAYERS[1].name]);
    var before=state.picks.length;
    applyLeague("espn10");
    applyLeague("sleeper12");
    if(state.picks.length!==before)
      throw new Error("came back with "+state.picks.length+" of "+before+" picks");
    clearPlaceholders();
  });

  await astep("a-finished-draft-does-not-announce-a-clock",async function(){
    /* Replaying a completed draft ended with "you are on the clock" after the final
       pick. A finished draft must read as finished. */
    setDraftId("sleeper12","999");
    applyLeague("sleeper12");
    state.picks=[]; state.sim=false;
    var n=totalPicks();
    var pool=PLAYERS.slice().sort(function(a,b){return a.adp-b.adp;});
    var feed=[];
    for(var i=0;i<n;i++){
      var p=pool[i];
      var c=(p?p.name:("Unknown Person "+i)).split(" ");
      feed.push({pick_no:i+1, metadata:{first_name:c[0], last_name:c.slice(1).join(" ")}});
    }
    var real=window.fetch;
    window.fetch=function(){ return Promise.resolve({ok:true,status:200,
      json:function(){ return Promise.resolve(feed); }}); };
    LIVE_SYNC={timer:null,key:"sleeper12",last:-1,fails:0,at:0};
    try{ await liveSyncTick(); } finally { window.fetch=real; }
    var msg=document.getElementById("liveMsg").textContent;
    if(msg.indexOf("on the clock")>=0)
      throw new Error("announced a clock after the last pick: "+msg);
    if(msg.indexOf("complete")<0) throw new Error("did not say complete: "+msg);
    clearPlaceholders();
  });

  step("a-mock-is-a-contest-not-a-demonstration",function(){
    /* The symptom that started this: twelve MFL mocks put my team first in eleven of
       them. aiPick chose on ADP and need alone while recommend() optimises vorp and
       proj, and rosters are then scored by proj - so the field was playing a different
       game from the one being marked. Testing the field's scoring function directly
       proved too loose to catch that (the top player by ADP is usually the top player
       by value too), so this asserts the outcome instead, which is what actually
       matters and what actually broke. */
    applyLeague("mfl12");
    var firsts=0, trials=8;
    for(var k=0;k<trials;k++){
      state.slot=(k%12)+1; state.picks=[]; state.sim=true; state.seed=String(9000+k);
      var need=state.teams*state.rounds, g=0;
      runSim();
      while(state.picks.length<need && g++<800){
        var r=recommend(); if(!r.length) break; makePick(r[0].p.id); runSim();
      }
      var all=[]; for(var t=0;t<state.teams;t++) all.push(bestLineup(rosterOf(t)).points);
      var mine=bestLineup(rosterOf(myIdx())).points;
      if(Math.max.apply(null,all) === mine) firsts++;
    }
    /* A good tool should win more than its share of a twelve-team room, but winning
       nearly every time means the field is not competing. */
    if(firsts/trials > 0.6)
      throw new Error("recommender finished first in "+firsts+"/"+trials+" mocks");
    state.picks=[]; state.sim=false;
  });

  step("every-league-can-actually-fill-its-roster-rules",function(){
    /* CBS makes you roster two of every position - 24 kickers and 24 defenses across
       a 12-team room - while the built-in board carried ten kickers. Nine of twelve
       seats could not finish legally, and the offline board is exactly what he falls
       back on if the wifi dies mid-draft. */
    ["espn10","cbs12","mfl12","sleeper12"].forEach(function(lg){
      applyLeague(lg);
      Object.keys(NEED).forEach(function(pos){
        var pool = PLAYERS.filter(function(p){ return p.pos===pos; }).length;
        var wanted = NEED[pos] * state.teams;
        if(pool < wanted)
          throw new Error(lg+" needs "+wanted+" "+pos+" but the board has "+pool);
      });
    });
  });

  step("a-full-draft-finishes-legal-in-every-league",function(){
    /* Roster minimums are a rule the commissioner enforces, not a preference to be
       outvoted by a projection. Once the picks left equal the requirements still
       owed, every remaining pick is committed.

       The tight case is what makes this real. With sixteen rounds there is enough
       slack that the soft need weight happens to cope; squeeze CBS down to twelve -
       exactly its twelve required spots - and without the hard gate 22 of 36 drafts
       finish short, almost all of them missing a kicker. The app has a rounds
       control, so this is a state a user can reach. */
    var cases = [["espn10",null],["mfl12",null],["cbs12",null],["cbs12",12]];
    cases.forEach(function(c){
      var lg=c[0], forceRounds=c[1];
      applyLeague(lg);
      if(forceRounds) state.rounds=forceRounds;
      var seats=[];
      if(lg==="cbs12"){ for(var s=1;s<=state.teams;s++) seats.push(s); }
      else seats=[1, Math.ceil(state.teams/2), state.teams];
      seats.forEach(function(seat){
        state.slot=seat; state.picks=[]; state.sim=true; state.seed=String(600+seat*11);
        var need=state.teams*state.rounds, g=0;
        runSim();
        while(state.picks.length<need && g++<900){
          var r=recommend(); if(!r.length) break; makePick(r[0].p.id); runSim();
        }
        var roster=rosterOf(myIdx());
        Object.keys(NEED).forEach(function(pos){
          var have=roster.filter(function(p){ return p.pos===pos; }).length;
          if(have < NEED[pos])
            throw new Error(lg+(forceRounds?" @"+forceRounds+"rd":"")+" seat "+seat+
                            " finished with "+have+" "+pos+", needs "+NEED[pos]);
        });
      });
    });
    state.picks=[]; state.sim=false;
    applyLeague("sleeper12");
  });

  step("no-reach-penalty-for-a-player-who-cannot-last",function(){
    /* Reaching only wastes a pick if he might have been there next time. At Robert's
       third overall pick, with the top two backs gone, McCaffrey was worth 131 over
       replacement to Nacua's 113 - taking the back and filling receiver later is worth
       about 18 roster points - and the board took Nacua anyway, by 3%, purely because
       Nacua goes at ADP 3.1 and McCaffrey at 6.3, so "reaching" three picks cost 14%.
       The same loop had McCaffrey surviving to the next pick 0% of the time. The two
       terms were arguing and the wrong one won.

       Stated without naming players: if A is clearly worth more than B, A goes later
       in ADP than B, and NEITHER can survive to my next pick, then A must be ranked
       first. There is no version of waiting that gets me A. */
    applyLeague("mfl12");
    state.picks=[]; state.sim=false; state.slot=3;
    /* Clear the two most valuable players, which is the situation at his real third
       pick: the elite backs are gone and the choice is the next back against the top
       receiver. While those two are still on the board McCaffrey is correctly marked
       down for being the third back available, so the fault does not appear. */
    var byVor = PLAYERS.slice().sort(function(a,b){ return (b.vorp||0)-(a.vorp||0); });
    makePick(byVor[0].id); makePick(byVor[1].id);
    var rec = recommend();
    if(rec.length < 4) throw new Error("too few recommendations");
    var here = state.picks.length + 1;
    var nextMine = null;
    for(var ov=here; ov<totalPicks(); ov++) if(teamOnClock(ov)===myIdx()){ nextMine=ov; break; }
    var pool = rec.slice(0, 10).map(function(r,idx){
      return {p:r.p, order:idx, surv:survival(r.p, here, nextMine===null?null:nextMine+1)};
    }).filter(function(x){ return x.surv < 0.05; });
    var checked = 0;
    pool.forEach(function(a){
      pool.forEach(function(b){
        if(a===b) return;
        if((a.p.vorp||0) < (b.p.vorp||0) + 12) return;   // A must be clearly better
        if(a.p.adp <= b.p.adp) return;                   // and A must be the "reach"
        checked++;
        if(a.order > b.order)
          throw new Error("ranked "+b.p.name+" ("+Math.round(b.p.vorp)+", adp "+
            b.p.adp.toFixed(1)+") above "+a.p.name+" ("+Math.round(a.p.vorp)+", adp "+
            a.p.adp.toFixed(1)+") though neither can last");
      });
    });
    if(!checked) throw new Error("no comparable pair found - test proves nothing");
    state.picks=[]; state.sim=false;
  });

  step("rounds-control-can-express-every-league",function(){
    /* The options were hard-coded 13-16, so for a 12-round league the control rendered
       blank and the only thing it could do was lengthen the draft. */
    Object.keys(LEAGUES).forEach(function(k){
      applyLeague(k);
      var sel=document.getElementById("rounds");
      var vals=[].slice.call(sel.options).map(function(o){ return +o.value; });
      if(vals.indexOf(state.rounds)<0)
        throw new Error(k+" drafts "+state.rounds+" rounds, options are "+vals.join(","));
      if(+sel.value !== state.rounds)
        throw new Error(k+" shows "+JSON.stringify(sel.value)+", expected "+state.rounds);
    });
  });

  step("a-device-can-hand-its-setup-to-another",function(){
    /* The app has read a #setup= link since it left the artifact, so nobody has to
       retype a 19-digit draft id on a phone - but nothing ever wrote one, so the
       honest answer to "how do I use this on my phone" was to assemble JSON by hand.
       Round-trip it: build the link here, wipe the device, feed the link back. */
    applyLeague("sleeper12");
    setDraftId("sleeper12","1234567890123456789");
    setDraftWhen("sleeper12","2026-08-28T18:30");
    setDraftId("mfl12","");
    setDraftWhen("mfl12","2026-08-29T12:30");
    var url = setupLink();
    if(!url) throw new Error("no link built");
    if(url.indexOf("#setup=") < 0) throw new Error("not a setup link");

    setDraftId("sleeper12","");
    setDraftWhen("sleeper12","");
    setDraftWhen("mfl12","");
    if(draftIdFor("sleeper12")) throw new Error("wipe failed");

    var res = applySetupHash(url.slice(url.indexOf("#")));
    if(!res || res.error) throw new Error("link rejected: "+(res && res.error));
    if(draftIdFor("sleeper12") !== "1234567890123456789")
      throw new Error("draft id did not survive: "+draftIdFor("sleeper12"));
    if(draftWhenFor("mfl12") !== "2026-08-29T12:30")
      throw new Error("draft time did not survive: "+draftWhenFor("mfl12"));
  });

  step("the-order-link-carries-a-non-snake-order",function(){
    /* His MFL order is the thing least worth retyping - 144 slots that are not a
       snake after round two. */
    applyLeague("mfl12");
    var ord = [];
    for(var i=0;i<144;i++) ord.push((i*5+3) % 12);      // deliberately not a snake
    setDraftOrder(ord);
    var url = orderLink();
    if(!url) throw new Error("no order link built");
    setDraftOrder(null);
    var res = applyMflHash(url.slice(url.indexOf("#")));
    if(!res || res.error) throw new Error("order link rejected: "+(res && res.error));
    if(!state.order || state.order.length !== 144)
      throw new Error("order did not survive: "+(state.order && state.order.length));
    for(var k=0;k<144;k++)
      if(state.order[k] !== ord[k]) throw new Error("slot "+k+" changed");
    setDraftOrder(null);
  });

  step("rivals-are-named-once-we-know-them",function(){
    /* Every rival read "Team 8" or "T8", which is useless in a room where you know
       these people by name. */
    applyLeague("mfl12");
    state.picks=[]; state.sim=false; state.slot=1;
    delete ROOM.mfl12;
    var before = teamName(7);
    if(before !== "Team 8") throw new Error("unnamed team should read Team 8, got "+before);
    if(teamTag(7) !== "T8") throw new Error("unnamed tag should read T8, got "+teamTag(7));

    var made = [];
    for(var i=0;i<12;i++) made.push("Placeholder Squad " + (i+1));
    var n = setRoomNames("mfl12", made);
    if(n !== 12) throw new Error("saved "+n+" of 12");
    if(teamName(7) !== "Placeholder Squad 8")
      throw new Error("name not used: "+teamName(7));
    if(teamTag(7) !== "PS") throw new Error("tag should initial down to PS, got "+teamTag(7));

    /* And it must actually reach the screen. */
    state.tab = "draft";
    renderAll();
    var shown = document.getElementById("p-draft").textContent;
    if(shown.indexOf("Placeholder Squad") < 0 && shown.indexOf("PS") < 0)
      throw new Error("names never rendered on the draft tab");
    delete ROOM.mfl12; saveRoom(); renderAll();
  });

  step("the-mfl-link-reports-the-names-it-saved",function(){
    /* The count was computed and then thrown away: the note hung on a variable that
       is overwritten whenever an order is present, which is always, because the names
       travel with the order. */
    delete ROOM.mfl12; saveRoom();
    applyLeague("mfl12");
    var ord=[]; for(var i=0;i<24;i++) ord.push(i%12);
    var teams=[]; for(var j=0;j<12;j++) teams.push("Squad "+(j+1));
    var res=applyMflHash("#mfl="+encodeURIComponent(JSON.stringify(
      {league:"mfl12", order:ord, names:[], teams:teams})));
    if(!res || res.error) throw new Error("rejected: "+(res&&res.error));
    if(res.applied.indexOf("12 team names")<0)
      throw new Error("did not report the names: "+res.applied);
    if(res.applied.indexOf("rounds")<0)
      throw new Error("stopped reporting the order: "+res.applied);
    if(!ROOM.mfl12 || ROOM.mfl12[5]!=="Squad 6") throw new Error("names not stored");
    delete ROOM.mfl12; saveRoom(); setDraftOrder(null);
  });

  step("room-names-are-scoped-to-one-league",function(){
    /* Twelve MFL managers must not become the ten ESPN ones. */
    delete ROOM.mfl12; delete ROOM.espn10;
    setRoomNames("mfl12", ["Alpha","Bravo","Charlie","Delta","Echo","Foxtrot",
                           "Golf","Hotel","India","Juliet","Kilo","Lima"]);
    applyLeague("espn10");
    if(teamName(0) !== "Team 1")
      throw new Error("espn borrowed an MFL name: "+teamName(0));
    applyLeague("mfl12");
    if(teamName(0) !== "Alpha") throw new Error("mfl lost its own: "+teamName(0));
    /* Never store more names than the league has seats. */
    var over = [];
    for(var i=0;i<40;i++) over.push("X"+i);
    setRoomNames("espn10", over);
    if(ROOM.espn10.length > LEAGUES.espn10.teams)
      throw new Error("stored "+ROOM.espn10.length+" names for a 10-team league");
    delete ROOM.mfl12; delete ROOM.espn10; saveRoom();
  });

  step("no-league-identity-is-baked-into-the-build",function(){
    /* Names live on the device, never in the source. The published board carries no
       league identity and adding this must not change that. */
    delete ROOM.mfl12; saveRoom();
    var src = document.documentElement.outerHTML;
    var marker = String.fromCharCode(82,79,79,77,95,75,69,89);   // ROOM_KEY
    if(src.indexOf(marker) < 0) throw new Error("room store missing entirely");
    /* The store must start empty in a clean build - nothing pre-populated. */
    if(ROOM.mfl12 || ROOM.espn10 || ROOM.cbs12 || ROOM.sleeper12)
      throw new Error("a league shipped with names already in it");
  });

  step("no-host-league-number-is-baked-in",function(){
    /* The published board carries no league identity. The Sleeper draft id already
       lived in localStorage; the MyFantasyLeague league number was hard-coded twice
       and slipped past the existing guards, which only looked for draft ids and
       league names. */
    var src = document.documentElement.outerHTML;
    var m = src.match(/myfantasyleague\.com[^"'`<]*[?&]L=(\d+)/i);
    if(m) throw new Error("a MyFantasyLeague league number is baked in: L=" + m[1]);
    /* And the bookmarklet must refuse rather than invent one. */
    applyLeague("mfl12");
    var had = draftIdFor("mfl12");
    setDraftId("mfl12", "");
    refreshBookmarklet("mfl12");
    var code = document.getElementById("bmCode").value;
    if(/[?&]L=\d/.test(code))
      throw new Error("bookmarklet built a league URL with no id saved");
    if(code.indexOf("league ID") < 0)
      throw new Error("bookmarklet gave no useful message: " + code.slice(0, 60));
    /* With an id, it uses that one and no other. */
    setDraftId("mfl12", "99999");
    refreshBookmarklet("mfl12");
    code = document.getElementById("bmCode").value;
    if(code.indexOf("L=99999") < 0) throw new Error("stored league id not used");
    setDraftId("mfl12", had);
    refreshBookmarklet("mfl12");
  });

  step("only-one-poller-exists",function(){
    /* Two implementations were once bound to the same checkbox, both polling and both
       writing state.picks. Anything named like a second one is a regression. */
    if(typeof window.livePoll === "function" || typeof window.liveToggle === "function")
      throw new Error("a second poller is present");
  });

  step("league-switch-stops-the-poller",function(){
    LIVE_SYNC={timer:setInterval(function(){},100000),key:"sleeper12",last:3,fails:0,at:0};
    applyLeague("espn10");
    if(LIVE_SYNC.timer) throw new Error("poller survived a league switch");
    if(LIVE_SYNC.key==="sleeper12") throw new Error("still pointed at the old draft");
  });

  step("live-sync-only-offered-where-a-feed-exists",function(){
    window.LIVE_CAPABLE=true;
    applyLeague("mfl12");
    if(!document.getElementById("liveWrap").hidden)
      throw new Error("offered live sync for a league with no public feed");
    applyLeague("sleeper12");
    if(document.getElementById("liveWrap").hidden)
      throw new Error("hid live sync for Sleeper");
  });

  var pre=document.createElement("pre"); pre.id="TESTLOG";
  pre.textContent=log.join(" | ")+"  ||ERRS:"+(window.__errs||[]).join(";");
  document.body.appendChild(pre);
})();
</script>
'''

open(_outfile,"w",encoding="utf-8").write(guard + src + fixture_js() + harness + '\n<script>\n/* Independent of the suite: if the harness itself dies, say why. */\nsetTimeout(function(){\n  if(document.getElementById("TESTLOG")) return;\n  var pre=document.createElement("pre"); pre.id="CRASHLOG";\n  pre.textContent = "HARNESS DID NOT FINISH\nerrors: " +\n    ((window.__errs && window.__errs.length) ? window.__errs.join(" | ") : "(none recorded)");\n  document.body.appendChild(pre);\n}, 60000);\n</script>\n')
print("harness written:", _outfile, "from", _srcfile)
