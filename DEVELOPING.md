# Working on The War Room

Everything the app needs is in `index.html` — one self-contained file, no build step, no
dependencies. Edit it, commit, push; GitHub Pages redeploys in about 40 seconds.

## Layout

| File | What it is |
|---|---|
| `index.html` | The whole app: data, engine, UI, styles |
| `manifest.webmanifest`, `sw.js`, `icon-*.png` | PWA shell — installable, works offline |

Inside `index.html`, in order: three baked ADP boards → season projections → the 2026
schedule → per-league scoring and roster rules → the engine → the views → boot.

## The leagues

Four are configured in `LEAGUES`. Each carries its own ADP board, scoring, starting lineup,
roster minimums, playoff weeks and strategy write-up. They are labelled by platform and
format only — no league names, no ids. **Anything that identifies a specific private league
belongs in device-local `localStorage`, never in this repo.** The Sleeper draft id lives
under `warroom.draftIds.v1` and is entered through the Sync panel.

Two separate concepts that are easy to conflate:

- `need` — how many of a position the rules make you **roster**
- `STARTERS` — how many you can actually **start**, derived from `LINEUP` with flex shared out

Value over replacement must use `STARTERS`. Using `need` once priced 24 quarterbacks as
starters in a 12-team league (the league requires two rostered but starts one) and inflated
every quarterback on the board.

## Data

All of it is public and CORS-open, so the page fetches its own updates:

- Projections: `api.sleeper.com/projections/nfl/2026?season_type=regular&position[]=RB`
- Weekly: `api.sleeper.com/projections/nfl/2026/{week}?...` — includes an `opponent` field
- Live draft picks: `api.sleeper.app/v1/draft/{id}/picks`
- Schedule: `api.sleeper.app/schedule/nfl/regular/2026`
- Current week: `api.sleeper.app/v1/state/nfl`

Baked data is the offline fallback; live data overrides it and is cached in `localStorage`.

Two source quirks worth knowing. Fantasy Football Calculator serves **one table per scoring
format** and silently ignores the team-count in its URL, so there is no league-size-specific
board. And Sleeper strips generational suffixes — it sends "Brian Thomas" where ADP boards
carry "Brian Thomas Jr." — which is why every lookup goes through `normName()`.

Kickers are `K` in Sleeper and `PK` on the ADP boards. That mismatch once meant no kicker
had a projection at all, hidden behind a coverage test with too low a threshold.

## Testing

There is no test runner. The suite is a script appended to a copy of the page, executed in
headless Chrome, which writes results into a `<pre>` that gets grepped out of the DOM. It
catches syntax errors, runtime errors and behaviour in one pass.

```
python mkharness.py                        # builds test-harness.html
chrome --headless=old --disable-gpu --no-sandbox \
       --virtual-time-budget=300000 --dump-dom test-harness.html > out.html
```

Then read the `TESTLOG` block. 76 assertions at the time of writing.

Traps that have each cost a debugging cycle:

- `applyLeague()` clears `state.picks`. Any test that inspects a roster must draft *after*
  switching leagues — use the `ensureDraft()` helper.
- `makePick()` assigns to whoever is on the clock, not to you. To force players onto your
  own roster in a test, push into `state.picks` with `team: myIdx()`.
- Generating JavaScript from Python patch scripts eats backslashes. An escaped apostrophe or
  a `'\n'` becomes a literal and breaks the entire script. Avoid escapes in generated
  strings; the harness reports `e.lineno`/`e.colno`, which finds them in one run.
- A test that scans the DOM for a string will match its own source. Split the literal.

## Principles worth keeping

Projections are real or absent — never invented. Where a rule cannot be derived from the
available data (per-game bonus ladders, distance-scaled touchdowns), the app says so in the
scoring `caveat` rather than guessing. Where a number is modelled rather than measured
(survival odds, strength of schedule), it is labelled as odds or as a proxy. That honesty is
the point of the tool: a board that looks more precise than it is will lose you a draft.
