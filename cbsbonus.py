# -*- coding: utf-8 -*-
"""What did CBS's bonus ladder actually pay in 2025, and by how much are we understating?"""
import json, os, subprocess, io, sys, statistics
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 Chrome/128.0"
os.makedirs("s25", exist_ok=True)

def fetch(week, pos):
    path = "s25/%s-%d.json" % (pos, week)
    if os.path.exists(path) and os.path.getsize(path) > 200:
        return path
    url = ("https://api.sleeper.com/stats/nfl/2025/%d?season_type=regular&position[]=%s"
           % (week, pos))
    subprocess.run(["curl", "-s", "-A", UA, "-o", path, url], check=False)
    return path

POSITIONS = ["QB", "RB", "WR", "TE"]
games = {}          # (name,pos) -> list of per-game dicts
for pos in POSITIONS:
    for wk in range(1, 19):
        p = fetch(wk, pos)
        try:
            data = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        for rec in data:
            pl = rec.get("player") or {}
            s = rec.get("stats") or {}
            nm = ((pl.get("first_name") or "") + " " + (pl.get("last_name") or "")).strip()
            if not nm:
                continue
            if not any(s.get(k) for k in ("pass_yd", "rush_yd", "rec_yd")):
                continue
            games.setdefault((nm, pos), []).append({
                "pass_yd": s.get("pass_yd", 0) or 0,
                "rush_yd": s.get("rush_yd", 0) or 0,
                "rec_yd":  s.get("rec_yd", 0) or 0,
                "pts_std": s.get("pts_std", 0) or 0,
            })

print("players with 2025 game logs:", len(games))

# CBS ladder, highest applicable tier only (the conservative reading)
def pass_bonus(y):
    for th, b in ((600,11),(550,10),(500,9),(450,8),(400,7),(350,6),(300,5),(250,4),(200,3)):
        if y >= th:
            return b
    return 0

def rush_rec_bonus(y):
    for th, b in ((350,8),(300,7),(250,6),(200,5),(150,4),(100,3)):
        if y >= th:
            return b
    return 0

rows = []
for (nm, pos), gl in games.items():
    if len(gl) < 6:
        continue
    pb = sum(pass_bonus(g["pass_yd"]) for g in gl)
    rb = sum(rush_rec_bonus(g["rush_yd"]) for g in gl)
    cb = sum(rush_rec_bonus(g["rec_yd"]) for g in gl)
    total = pb + rb + cb
    ypg = statistics.mean([g["pass_yd"] for g in gl]) if pos == "QB" else \
          statistics.mean([g["rush_yd"] + g["rec_yd"] for g in gl])
    rows.append({"name": nm, "pos": pos, "g": len(gl), "bonus": total,
                 "perGame": total / len(gl), "ypg": ypg,
                 "base": sum(g["pts_std"] for g in gl)})

for pos in POSITIONS:
    grp = sorted([r for r in rows if r["pos"] == pos], key=lambda r: -r["base"])
    top = grp[:24] if pos != "QB" else grp[:12]
    if not top:
        continue
    print("\n=== %s (top %d by 2025 standard points) ===" % (pos, len(top)))
    print("  median bonus over the season : %.0f pts" % statistics.median([r["bonus"] for r in top]))
    print("  median bonus per game        : %.2f pts" % statistics.median([r["perGame"] for r in top]))
    print("  as %% of base scoring         : %.1f%%" %
          (100 * sum(r["bonus"] for r in top) / max(1, sum(r["base"] for r in top))))
    for r in top[:5]:
        print("   %-24s %2dg  base %6.1f  bonus %5.1f  (%.2f/g, %.0f ypg)"
              % (r["name"], r["g"], r["base"], r["bonus"], r["perGame"], r["ypg"]))

# empirical curve: bonus per game as a function of yards per game
print("\n=== bonus per game by yards per game (this is the calibration) ===")
for pos, buckets in (("QB", [(0,150),(150,200),(200,225),(225,250),(250,275),(275,300),(300,999)]),
                     ("RB", [(0,40),(40,60),(60,80),(80,100),(100,999)]),
                     ("WR", [(0,40),(40,60),(60,80),(80,100),(100,999)]),
                     ("TE", [(0,30),(30,50),(50,70),(70,999)])):
    print(" " + pos + ":")
    for lo, hi in buckets:
        grp = [r for r in rows if r["pos"] == pos and lo <= r["ypg"] < hi]
        if len(grp) < 3:
            continue
        print("   %3d-%-3s ypg  n=%-3d  bonus/game %.2f"
              % (lo, (str(hi) if hi < 999 else "+"), len(grp),
                 statistics.mean([r["perGame"] for r in grp])))
