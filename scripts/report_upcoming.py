#!/usr/bin/env python3
"""Generate a full markdown report for the upcoming World Cup 2026 matchups.

Predicts each team's next unplayed group match from **current Elo**, compares to
the de-vigged market, and writes a presentable report with an overview heatmap
grid, a summary table, the biggest model-vs-market disagreements, and a detailed
card per fixture.

    python scripts/report_upcoming.py            # next matchday (the openers now)
    python scripts/report_upcoming.py --all       # all remaining group games
    python scripts/report_upcoming.py --refresh    # pull latest results first

Writes reports/wc2026_upcoming.md (+ figures under reports/figures/wc2026/).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

from wcmodel import backtest as bt, data, matrix as mx, odds  # noqa: E402
from wcmodel.forward import current_ratings, load_schedule, next_round, refresh_snapshot  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

REPORTS = data.ROOT / "reports"
FIG_DIR = REPORTS / "figures" / "wc2026"
FORWARD_LOG = data.DATA / "external" / "wc2026_forward_log.csv"
GREENRED = LinearSegmentedColormap.from_list("greenred", ["#1a9850", "#ffffbf", "#d73027"])
EDGE_THRESHOLD = 0.10


def _predict_all(model, fixtures, snap, market):
    """Build the per-fixture prediction records."""
    recs = []
    for i, fx in enumerate(fixtures.itertuples(index=False)):
        h, a, neutral = fx.home_team, fx.away_team, bool(fx.neutral)
        if h not in snap.index or a not in snap.index:
            continue
        lam, mu = model.fixture_lambdas(snap, h, a, neutral=neutral)
        M = mx.score_matrix(lam, mu, model.rho)
        d = mx.derived_markets(M)
        mkt = market[i] if market is not None else np.array([np.nan, np.nan, np.nan])
        ours = np.array([d["p_home"], d["p_draw"], d["p_away"]])
        edge = float(np.nanmax(np.abs(ours - mkt))) if not np.isnan(mkt).all() else np.nan
        recs.append({
            "date": pd.Timestamp(fx.date), "home": h, "away": a, "neutral": neutral,
            "elo_h": float(snap[h]), "elo_a": float(snap[a]),
            "lam": lam, "mu": mu, "matrix": M,
            "pH": d["p_home"], "pD": d["p_draw"], "pA": d["p_away"],
            "over25": d["p_over_2_5"], "under25": d["p_under_2_5"], "btts": d["btts_yes"],
            "mH": mkt[0], "mD": mkt[1], "mA": mkt[2], "edge": edge,
            "top5": d["top5_scores"],
        })
    return recs


def _overview_grid(recs, path):
    """A contact sheet: one mini score-matrix heatmap per fixture."""
    n = len(recs)
    cols = 4
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.5 * rows))
    axes = np.atleast_1d(axes).ravel()
    for ax, r in zip(axes, recs):
        sub = r["matrix"][:7, :7]
        ax.imshow(sub, cmap=GREENRED, vmin=0, vmax=sub.max())
        (mh, ma), _ = r["top5"][0]
        ax.set_title(f"{r['home']} v {r['away']}\n{mh}-{ma}  ·  "
                     f"{r['pH']*100:.0f}/{r['pD']*100:.0f}/{r['pA']*100:.0f}", fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel(f"{r['away'][:12]} →", fontsize=7)
        ax.set_ylabel(f"{r['home'][:12]} →", fontsize=7)
    for ax in axes[len(recs):]:
        ax.axis("off")
    fig.suptitle("2026 World Cup — predicted score grids (rows = home goals, cols = away goals)",
                 fontsize=13, y=1.002)
    fig.tight_layout()
    fig.savefig(path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def _marquee_heatmap(rec, path):
    fig, ax = plt.subplots(figsize=(6.5, 6))
    mx.render_matrix(rec["matrix"], rec["home"], rec["away"], rec["lam"], rec["mu"], ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _fav_line(r):
    """One-line read combining model lean and market agreement."""
    fav = r["home"] if r["pH"] >= r["pA"] else r["away"]
    favp = max(r["pH"], r["pA"])
    base = f"{fav} favoured ({favp*100:.0f}%)"
    if np.isnan(r["edge"]):
        return base + "."
    if r["edge"] < EDGE_THRESHOLD:
        return base + "; in line with the market."
    side = "higher" if (r["pH"] - r["mH"]) > 0 else "lower"
    return base + f"; **model {side} than the market on {r['home']}** (Δ{r['edge']*100:.0f}pp)."


def _results_scorecard(A) -> None:
    """Completed-match scorecard from the forward log: model call vs market vs result."""
    if not FORWARD_LOG.exists():
        return
    log = pd.read_csv(FORWARD_LOG)
    done = log[log["outcome_idx"].notna()].copy()
    if done.empty:
        return
    names = {0: "home", 1: "draw", 2: "away"}
    A("## Results so far\n")
    A("How the pre-match forecasts have fared, model vs de-vigged market "
      "(this is the B2 baseline, scored live going forward):\n")
    A("| Match | Result | Our call (H/D/A) | Market (H/D/A) | Winner |")
    A("|---|---|---|---|---|")
    m_rps, k_rps = [], []
    for r in done.itertuples(index=False):
        o = int(r.outcome_idx)
        our = np.array([r.p_home, r.p_draw, r.p_away])
        mkt = np.array([r.mkt_home, r.mkt_draw, r.mkt_away])
        mr, kr = bt.rps(our, o), bt.rps(mkt, o)
        m_rps.append(mr); k_rps.append(kr)
        sharper = "model" if mr < kr else ("market" if kr < mr else "tie")
        A(f"| {r.home_team} v {r.away_team} | {int(r.home_score)}-{int(r.away_score)} "
          f"({names[o]}) | {r.p_home*100:.0f}/{r.p_draw*100:.0f}/{r.p_away*100:.0f} | "
          f"{r.mkt_home*100:.0f}/{r.mkt_draw*100:.0f}/{r.mkt_away*100:.0f} | {sharper} |")
    A("")
    mm, kk = float(np.mean(m_rps)), float(np.mean(k_rps))
    lead = "model ahead" if mm < kk else ("market ahead" if kk < mm else "level")
    A(f"**Running RPS over {len(done)} match(es): model {mm:.4f} vs market {kk:.4f} "
      f"— {lead}.** (Tiny sample — a smoke signal, not a verdict.)\n")


def _write_report(recs, as_of, have_mkt, path, label):
    L = []
    A = L.append
    A(f"# World Cup 2026 — {label}\n")
    A(f"Model-based forecasts for the next round of group matches "
      f"({len(recs)} fixtures), generated from **current Elo** "
      f"(all played matches through {as_of:%Y-%m-%d}). The Dixon-Coles Poisson "
      f"model is the one validated on the 2018 & 2022 backtests; its coefficients "
      f"are frozen at the 2022-11-19 fit, only the ratings are current.\n")
    if have_mkt:
        A("De-vigged bookmaker odds are shown for comparison only — they do **not** "
          "feed the model. `Edge` = largest gap between our probability and the "
          "market on any outcome.\n")

    _results_scorecard(A)

    A("![overview](figures/wc2026/overview.png)\n")

    # Summary table
    A("## All fixtures\n")
    cols = "| Date | Match | Venue | xG (H–A) | Our H/D/A | "
    cols += "Market H/D/A | Edge | Top score |" if have_mkt else "O2.5 | BTTS | Top score |"
    A(cols)
    A("|---|---|---|---|---|---|" + ("---|---|" if have_mkt else "---|---|"))
    for r in sorted(recs, key=lambda x: x["date"]):
        (mh, ma), _ = r["top5"][0]
        venue = "neutral" if r["neutral"] else f"{r['home']} (H)"
        our = f"{r['pH']*100:.0f}/{r['pD']*100:.0f}/{r['pA']*100:.0f}"
        if have_mkt:
            mk = "—" if np.isnan(r["mH"]) else f"{r['mH']*100:.0f}/{r['mD']*100:.0f}/{r['mA']*100:.0f}"
            edge = "—" if np.isnan(r["edge"]) else f"{r['edge']*100:.0f}pp"
            A(f"| {r['date']:%b %d} | {r['home']} v {r['away']} | {venue} | "
              f"{r['lam']:.2f}–{r['mu']:.2f} | {our} | {mk} | {edge} | {mh}-{ma} |")
        else:
            A(f"| {r['date']:%b %d} | {r['home']} v {r['away']} | {venue} | "
              f"{r['lam']:.2f}–{r['mu']:.2f} | {our} | {r['over25']*100:.0f}% | "
              f"{r['btts']*100:.0f}% | {mh}-{ma} |")
    A("")

    # Edges
    if have_mkt:
        edges = sorted([r for r in recs if not np.isnan(r["edge"]) and r["edge"] >= EDGE_THRESHOLD],
                       key=lambda x: -x["edge"])
        A("## Where we disagree with the market\n")
        if edges:
            A("The model is independent of the odds, so these gaps are where our "
              "Elo-Poisson view parts from the bookmaker — and they cluster on the "
              "model's known soft spots (host-advantage calibration; less boldness "
              "on big favourites).\n")
            A("| Match | Our H/D/A | Market H/D/A | Edge | Lean |")
            A("|---|---|---|---|---|")
            for r in edges:
                side = "higher" if (r["pH"] - r["mH"]) > 0 else "lower"
                A(f"| {r['home']} v {r['away']} | "
                  f"{r['pH']*100:.0f}/{r['pD']*100:.0f}/{r['pA']*100:.0f} | "
                  f"{r['mH']*100:.0f}/{r['mD']*100:.0f}/{r['mA']*100:.0f} | "
                  f"{r['edge']*100:.0f}pp | model {side} on {r['home']} |")
            A("")
        else:
            A("No fixture disagrees with the market by ≥10pp on any outcome.\n")

    # Per-match cards
    A("## Match-by-match\n")
    cur_date = None
    for r in sorted(recs, key=lambda x: (x["date"], x["home"])):
        if r["date"] != cur_date:
            cur_date = r["date"]
            A(f"### {r['date']:%A, %B %d}\n")
        venue = "neutral venue" if r["neutral"] else f"{r['home']} at home"
        A(f"**{r['home']} vs {r['away']}** — _{venue}_  ")
        A(f"Elo {r['home']} {r['elo_h']:.0f} · {r['away']} {r['elo_a']:.0f}  |  "
          f"expected goals **{r['lam']:.2f} – {r['mu']:.2f}**  ")
        A(f"- **1X2:** {r['home']} {r['pH']*100:.0f}% · Draw {r['pD']*100:.0f}% · "
          f"{r['away']} {r['pA']*100:.0f}%"
          + (f"   _(market {r['mH']*100:.0f}/{r['mD']*100:.0f}/{r['mA']*100:.0f})_"
             if have_mkt and not np.isnan(r["mH"]) else ""))
        A(f"- **Goals:** Over 2.5 {r['over25']*100:.0f}% · BTTS {r['btts']*100:.0f}%")
        scores = " · ".join(f"{i}-{j} {p*100:.0f}%" for (i, j), p in r["top5"][:5])
        A(f"- **Likeliest scores:** {scores}")
        A(f"- {_fav_line(r)}\n")

    # Caveats
    A("---")
    A("## How to read this & caveats\n")
    A("- **1X2 is the trustworthy output.** Goal totals run a touch low — the "
      "model under-predicts blowouts (a known, documented bias whose fix didn't "
      "generalize across backtests), so treat Over/Under as soft.\n")
    A("- **Group stage only.** Knockouts (extra time / penalties) are out of scope.\n")
    A("- **Market is a benchmark, not an input.** Where we disagree, the market is "
      "usually the sharper number; the gaps are flagged so you can judge for yourself.\n")
    A(f"- _Generated {pd.Timestamp.today():%Y-%m-%d} · Elo current to {as_of:%Y-%m-%d} "
      f"· model frozen 2022-11-19._")

    path.write_text("\n".join(L))


def main() -> None:
    ap = argparse.ArgumentParser(description="Full report for upcoming WC2026 matchups.")
    ap.add_argument("--all", action="store_true", help="all remaining group games")
    ap.add_argument("--refresh", action="store_true", help="re-download results first")
    ap.add_argument("--odds", default=str(data.DATA / "external" / "wc2026_odds.csv"))
    ap.add_argument("--model", default=str(data.PROCESSED / "model.json"))
    args = ap.parse_args()

    if args.refresh:
        refresh_snapshot()

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    model = FittedModel.load(args.model)
    played, upcoming = load_schedule()
    if upcoming.empty:
        raise SystemExit("No upcoming FIFA World Cup fixtures in the snapshot.")
    fixtures = upcoming if args.all else next_round(upcoming)
    snap, as_of = current_ratings(played)
    market = odds.load_market(fixtures, args.odds)
    have_mkt = market is not None

    recs = _predict_all(model, fixtures, snap, market)

    # Figures: overview grid + a few marquee heatmaps.
    _overview_grid(recs, FIG_DIR / "overview.png")
    by_fav = sorted(recs, key=lambda r: -max(r["pH"], r["pA"]))
    marquee = [recs[0]]  # the opener
    if have_mkt:
        marquee.append(max(recs, key=lambda r: (r["edge"] if r["edge"] == r["edge"] else -1)))
    marquee.append(by_fav[0])  # biggest favourite
    seen, picks = set(), []
    for r in marquee:
        k = (r["home"], r["away"])
        if k not in seen:
            seen.add(k); picks.append(r)
    for r in picks:
        _marquee_heatmap(r, FIG_DIR / f"{r['home']}_{r['away']}.png".replace(" ", "_"))

    span = sorted(recs, key=lambda x: x["date"])
    label = (f"Opening Matches ({span[0]['date']:%b %d}–{span[-1]['date']:%b %d})"
             if not args.all else "Remaining Group Games")
    out = REPORTS / "wc2026_upcoming.md"
    _write_report(recs, as_of, have_mkt, out, label)

    print(f"Wrote {out.relative_to(data.ROOT)}")
    print(f"  + figures/wc2026/overview.png and {len(picks)} marquee heatmap(s)")
    print(f"  {len(recs)} fixtures, Elo current to {as_of:%Y-%m-%d}")


if __name__ == "__main__":
    main()
