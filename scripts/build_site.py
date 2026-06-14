#!/usr/bin/env python3
"""Build a simple static page (docs/index.html) for the next 3 World Cup fixtures.

For each of the next 3 kickoffs it shows our model's 1X2 (probability + fair
decimal odds), the top-3 scorelines, and — when bookmaker odds are present —
the market price and the **value/EV** by our model (``our_prob * odds - 1``).
A small scorecard tracks model-vs-market RPS over completed games.

The page is self-contained (inline CSS) and mobile-first, made to be served by
GitHub Pages from the ``/docs`` folder.

    python scripts/build_site.py [--n 3] [--refresh]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import backtest as bt, data, elo, matrix as mx, odds  # noqa: E402
from wcmodel.forward import load_schedule, refresh_snapshot  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

EDGE_THRESHOLD_PAGE = 0.15
EDGE_MOMENTUM_ALPHA = 2.0

DOCS = data.ROOT / "docs"
FORWARD_LOG = data.DATA / "external" / "wc2026_odds.csv"  # (only used via odds module)
LOG = data.DATA / "external" / "wc2026_forward_log.csv"


def _fair(p: float) -> str:
    return f"{1/p:.2f}" if p > 0 else "—"


def _scorecard():
    if not LOG.exists():
        return None
    log = pd.read_csv(LOG)
    done = log[log["outcome_idx"].notna()]
    if done.empty:
        return None
    o = done["outcome_idx"].astype(int).to_numpy()
    m = float(np.mean([bt.rps(p, o[i]) for i, p in
                       enumerate(done[["p_home", "p_draw", "p_away"]].to_numpy())]))
    k = float(np.mean([bt.rps(p, o[i]) for i, p in
                       enumerate(done[["mkt_home", "mkt_draw", "mkt_away"]].to_numpy())]))
    return {"n": len(done), "model": m, "market": k}


def _score_grid(rec) -> str:
    M = rec["matrix"]  # 4×4 ndarray: M[home_goals, away_goals]
    top5_set = {(i, j) for (i, j), _ in rec["top5"][:3]}
    peak = float(M.max())
    home, away = rec["home"], rec["away"]

    def _cell(i, j):
        p = float(M[i, j])
        # Intensity 0-100 for background opacity
        intensity = int(p / peak * 100) if peak > 0 else 0
        highlight = " grid-top" if (i, j) in top5_set else ""
        return (f"<td class='gc{highlight}' style='--gi:{intensity}'>"
                f"{p*100:.1f}%</td>")

    header_cells = "".join(f"<th class='gah'>{j}</th>" for j in range(4))
    body_rows = ""
    for i in range(4):
        cells = "".join(_cell(i, j) for j in range(4))
        body_rows += f"<tr><th class='ghh'>{i}</th>{cells}</tr>"

    return f"""
      <div class="grid-wrap">
        <div class="grid-labels">
          <span class="gl-home">{home} goals →</span>
          <span class="gl-away">{away} goals ↓</span>
        </div>
        <table class="grid-tbl">
          <thead><tr><th></th>{header_cells}</tr></thead>
          <tbody>{body_rows}</tbody>
        </table>
        <div class="grid-note">rows = {home} · cols = {away} · top-3 scorelines highlighted</div>
      </div>"""


def _game_card(rec) -> str:
    rows = []
    labels = [(rec["home"], "pH", "mH", "dH"), ("Draw", "pD", "mD", "dD"),
              (rec["away"], "pA", "mA", "dA")]
    best_ev = rec.get("best_ev")
    for name, pk, mk, dk in labels:
        p = rec[pk]
        offered = rec.get(dk)
        if offered and offered == offered:
            ev = p * offered - 1
            ev_txt = f"<span class='ev {'pos' if ev > 0 else 'neg'}'>{ev*100:+.0f}%</span>"
            mkt_txt = f"{offered:.2f}"
        else:
            ev_txt, mkt_txt = "<span class='muted'>—</span>", "—"
        hot = " hot" if (best_ev and best_ev[0] == name and best_ev[1] > 0) else ""
        rows.append(
            f"<tr class='{hot.strip()}'><td class='team'>{name}</td>"
            f"<td>{p*100:.0f}%</td><td>{_fair(p)}</td><td>{mkt_txt}</td><td>{ev_txt}</td></tr>"
        )
    scores = "".join(f"<span class='chip'>{i}-{j} <b>{pp*100:.0f}%</b></span>"
                     for (i, j), pp in rec["top5"][:3])
    venue = "neutral venue" if rec["neutral"] else f"{rec['home']} at home"
    val = ""
    if best_ev and best_ev[1] > 0:
        # Honest framing: a model edge, not an endorsed bet. Host games sit in the
        # model's known-unreliable zone (host calibration), either direction.
        warn = (" <span class='warn'>— host game, model's host calibration is shaky</span>"
                if not rec["neutral"] else "")
        val = (f"<div class='edge'>Model's biggest gap vs book: <b>{best_ev[0]}</b> "
               f"(+{best_ev[1]*100:.0f}% EV by our numbers){warn}</div>")
    return f"""
    <div class="card">
      <div class="when">{rec['date']:%a %b %d} · {venue}</div>
      <div class="match"><span>{rec['home']}</span><span class="vs">v</span><span>{rec['away']}</span></div>
      {_score_grid(rec)}
      <table>
        <thead><tr><th></th><th>Our</th><th>Fair</th><th>Book</th><th>EV</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
      {val}
      <div class="scores">{scores}</div>
      <div class="meta">xG {rec['lam']:.2f}–{rec['mu']:.2f} · Over 2.5 {rec['over25']*100:.0f}% · BTTS {rec['btts']*100:.0f}%</div>
    </div>"""


def _probs3(model, ratings, h, a, neutral):
    lam, mu = model.fixture_lambdas(ratings, h, a, neutral=neutral)
    d = mx.derived_markets(mx.score_matrix(lam, mu, model.rho))
    return np.array([d["p_home"], d["p_draw"], d["p_away"]])


def _edges_section(model, upcoming, snap, elo_long, as_of, max_show=10):
    """Upcoming games where |model - market| >= threshold, with the 3 checks."""
    devig = odds.load_market(upcoming.reset_index(drop=True))
    if devig is None:
        return ""
    bonus = elo.momentum(elo_long, as_of, alpha=EDGE_MOMENTUM_ALPHA,
                         half_life_days=270, cap=120)
    eff = snap.add(bonus.reindex(snap.index).fillna(0.0))

    items = []
    for i, fx in enumerate(upcoming.itertuples(index=False)):
        h, a, neutral = fx.home_team, fx.away_team, bool(fx.neutral)
        if h not in snap.index or a not in snap.index or np.isnan(devig[i]).all():
            continue
        ours = _probs3(model, snap, h, a, neutral)
        edge = float(np.max(np.abs(ours - devig[i])))
        if edge < EDGE_THRESHOLD_PAGE:
            continue
        new_edge = float(np.max(np.abs(_probs3(model, eff, h, a, neutral) - devig[i])))
        if new_edge < edge - 0.02:
            form = "<span class='toward'>form may explain it</span>"
        elif new_edge > edge + 0.02:
            form = "<span class='away'>not a form story</span>"
        else:
            form = "<span class='muted'>form ≈ no change</span>"
        host = ""
        if not neutral:
            tag = "over" if ours[0] > devig[i][0] + 0.05 else (
                "under" if ours[0] < devig[i][0] - 0.05 else "≈")
            host = f"<span class='host'>HOST {h} ({tag})</span>"
        items.append((edge, f"""
        <div class="erow">
          <div class="etop"><b>{h} v {a}</b><span class="epp">{edge*100:.0f}pp</span></div>
          <div class="emid">{fx.date:%b %d} · ours {ours[0]*100:.0f}/{ours[1]*100:.0f}/{ours[2]*100:.0f}
               · mkt {devig[i][0]*100:.0f}/{devig[i][1]*100:.0f}/{devig[i][2]*100:.0f}</div>
          <div class="eflags">{host}{form}<span class="inj">🔍 check injuries</span></div>
        </div>"""))
    if not items:
        return ""
    items.sort(reverse=True, key=lambda t: t[0])
    body = "".join(h for _, h in items[:max_show])
    extra = f"<div class='emore'>+{len(items)-max_show} more</div>" if len(items) > max_show else ""
    return (f"<div class='edges'><div class='etitle'>⚠️ Big disagreements vs market "
            f"(≥{EDGE_THRESHOLD_PAGE*100:.0f}pp)</div>{body}{extra}"
            f"<div class='ehint'>Where we differ most — check injuries & host/form before trusting either side.</div></div>")


def build(n: int, refresh: bool) -> None:
    if refresh:
        refresh_snapshot()
    model = FittedModel.load(data.PROCESSED / "model.json")
    played, upcoming = load_schedule()
    if upcoming.empty:
        raise SystemExit("No upcoming fixtures.")
    fixtures = upcoming.head(n).reset_index(drop=True)
    elo_long = elo.compute_elo(played.sort_values("date", kind="mergesort"))
    as_of = played["date"].max() + pd.Timedelta(days=1)
    snap = elo.latest_ratings(elo_long, as_of)
    devig = odds.load_market(fixtures)
    decimal = odds.load_market_decimal(fixtures)

    recs = []
    for i, fx in enumerate(fixtures.itertuples(index=False)):
        h, a, neutral = fx.home_team, fx.away_team, bool(fx.neutral)
        if h not in snap.index or a not in snap.index:
            continue
        lam, mu = model.fixture_lambdas(snap, h, a, neutral=neutral)
        M = mx.score_matrix(lam, mu, model.rho)
        d = mx.derived_markets(M)
        dec = decimal[i] if decimal is not None else [np.nan, np.nan, np.nan]
        ours = [d["p_home"], d["p_draw"], d["p_away"]]
        # Best value outcome by model EV.
        evs = [(nm, ours[k] * dec[k] - 1) for k, nm in enumerate([h, "Draw", a])
               if dec[k] == dec[k]]
        best_ev = max(evs, key=lambda t: t[1]) if evs else None
        recs.append({
            "home": h, "away": a, "neutral": neutral, "date": pd.Timestamp(fx.date),
            "lam": lam, "mu": mu, "pH": d["p_home"], "pD": d["p_draw"], "pA": d["p_away"],
            "dH": dec[0], "dD": dec[1], "dA": dec[2],
            "over25": d["p_over_2_5"], "btts": d["btts_yes"], "top5": d["top5_scores"],
            "best_ev": best_ev, "matrix": M[:4, :4],
        })

    edges_html = _edges_section(model, upcoming, snap, elo_long, as_of)

    sc = _scorecard()
    sc_html = ""
    if sc:
        lead = "model" if sc["model"] < sc["market"] else "market"
        sc_html = (f"<div class='scorebar'>Forward record · {sc['n']} games · "
                   f"model RPS <b>{sc['model']:.3f}</b> vs market <b>{sc['market']:.3f}</b> "
                   f"<span class='{lead}'>({lead} ahead)</span></div>")

    cards = "".join(_game_card(r) for r in recs)
    html = _PAGE.format(
        updated=pd.Timestamp.now("UTC").strftime("%Y-%m-%d %H:%M UTC"),
        asof=f"{as_of:%Y-%m-%d}", scorecard=sc_html, cards=cards, n=len(recs),
        edges=edges_html,
    )
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote docs/index.html — next {len(recs)} fixtures, Elo to {as_of:%Y-%m-%d}")


_PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WC 2026 · Model vs Market</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#0f1115; color:#e8eaed; font:15px/1.4 -apple-system,Segoe UI,Roboto,sans-serif; }}
  header {{ padding:18px 16px 8px; }}
  h1 {{ font-size:19px; margin:0; }}
  .sub {{ color:#8b929c; font-size:12px; margin-top:4px; }}
  .scorebar {{ margin:10px 16px; padding:10px 12px; background:#171a21; border-radius:10px; font-size:13px; }}
  .scorebar .model {{ color:#37d67a; }} .scorebar .market {{ color:#f0a93b; }}
  .wrap {{ padding:8px 12px 40px; max-width:560px; margin:0 auto; }}
  .card {{ background:#171a21; border:1px solid #232733; border-radius:14px; padding:14px; margin:12px 0; }}
  .when {{ color:#8b929c; font-size:12px; }}
  .match {{ display:flex; align-items:center; gap:8px; font-size:18px; font-weight:600; margin:6px 0 10px; }}
  .match .vs {{ color:#5b626d; font-size:13px; font-weight:400; }}
  table {{ width:100%; border-collapse:collapse; font-size:14px; }}
  th {{ color:#8b929c; font-weight:500; text-align:right; padding:2px 6px; font-size:12px; }}
  th:first-child {{ text-align:left; }}
  td {{ text-align:right; padding:5px 6px; border-top:1px solid #232733; }}
  td.team {{ text-align:left; font-weight:500; }}
  tr.hot td {{ background:#13251a; }}
  .ev.pos {{ color:#37d67a; font-weight:600; }} .ev.neg {{ color:#6b7280; }}
  .muted {{ color:#5b626d; }}
  .edge {{ margin:10px 0 4px; padding:6px 10px; background:#1c1b12; border:1px solid #4a401d;
           border-radius:8px; color:#f0c34b; font-size:13px; }}
  .edge .warn {{ color:#e0894a; }}
  .scores {{ margin-top:10px; display:flex; gap:6px; flex-wrap:wrap; }}
  .chip {{ background:#232733; border-radius:20px; padding:3px 10px; font-size:12px; color:#c7ccd4; }}
  .meta {{ color:#8b929c; font-size:12px; margin-top:8px; }}
  .grid-wrap {{ margin:10px 0 14px; }}
  .grid-labels {{ display:flex; justify-content:space-between; font-size:11px; color:#8b929c; margin-bottom:4px; }}
  .grid-tbl {{ width:100%; border-collapse:collapse; table-layout:fixed; }}
  .grid-tbl th, .grid-tbl td {{ padding:6px 2px; text-align:center; font-size:12px; }}
  .ghh {{ color:#8b929c; font-weight:600; font-size:12px; width:20px; }}
  .gah {{ color:#8b929c; font-weight:600; font-size:12px; }}
  .gc {{ background:rgba(55,214,122,calc(var(--gi)*0.008)); color:#c7ccd4; border-radius:4px; }}
  .gc.grid-top {{ outline:1px solid #37d67a; color:#37d67a; font-weight:600; }}
  .grid-note {{ color:#5b626d; font-size:10px; margin-top:4px; text-align:center; }}
  .edges {{ margin:18px 0 6px; }}
  .etitle {{ font-size:15px; font-weight:600; color:#f0c34b; margin-bottom:8px; }}
  .erow {{ background:#171a21; border:1px solid #232733; border-left:3px solid #f0c34b;
           border-radius:10px; padding:10px 12px; margin:8px 0; }}
  .etop {{ display:flex; justify-content:space-between; font-size:15px; }}
  .etop .epp {{ color:#f0a93b; font-weight:700; }}
  .emid {{ color:#8b929c; font-size:12px; margin-top:3px; }}
  .eflags {{ margin-top:7px; display:flex; gap:6px; flex-wrap:wrap; font-size:11px; }}
  .eflags span {{ padding:2px 7px; border-radius:12px; background:#232733; }}
  .eflags .host {{ background:#2a1f12; color:#e0894a; }}
  .eflags .toward {{ background:#13251a; color:#37d67a; }}
  .eflags .away {{ color:#9aa1ab; }}
  .eflags .inj {{ background:#1c1b2a; color:#b9a7f0; }}
  .emore {{ color:#8b929c; font-size:12px; padding:4px; }}
  .ehint {{ color:#5b626d; font-size:11px; margin-top:6px; }}
  footer {{ color:#5b626d; font-size:11px; text-align:center; padding:20px 16px 40px; }}
</style></head>
<body>
  <header>
    <h1>⚽ World Cup 2026 — Model vs Market</h1>
    <div class="sub">Next {n} kickoffs · Dixon-Coles Poisson on current Elo (to {asof}) · updated {updated}</div>
  </header>
  {scorecard}
  <div class="wrap">{cards}{edges}</div>
  <footer>
    Our model is independent of the odds. <b>Fair</b> = 1/our probability;
    <b>EV</b> = our&nbsp;prob × book&nbsp;odds − 1 (positive ⇒ value by the model).
    1X2 is the model's strong suit; scorelines/totals run soft. Big edges often sit on the
    model's blind spots (host teams, heavy favourites) — sanity-check those. For personal use, not advice — betting carries risk.
  </footer>
</body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the static next-fixtures page.")
    ap.add_argument("--n", type=int, default=4, help="number of upcoming fixtures (default 4)")
    ap.add_argument("--refresh", action="store_true", help="pull latest results first")
    args = ap.parse_args()
    build(args.n, args.refresh)


if __name__ == "__main__":
    main()
