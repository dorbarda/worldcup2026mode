#!/usr/bin/env python3
"""Batch group-stage predictions for the 2026 World Cup, from current Elo.

Designed for an "update as we go" loop:

1. Each run computes Elo from **all played matches** in the snapshot (current).
2. By default it predicts **each team's next unplayed group match** — right now
   that's every team's opener (24 matches). Once those results are added to the
   snapshot and Elo updates, the same command rolls forward to the next matchday.
3. ``--refresh`` re-downloads the martj42 results snapshot first, so newly played
   matches flow into Elo automatically.

The model *coefficients* come from the frozen, backtest-validated 2022-11-19 fit;
the *ratings* are current. Knockouts are out of scope (no ET/penalties layer).

Examples:
    python scripts/predict_fixtures.py                 # each team's next match
    python scripts/predict_fixtures.py --refresh        # pull latest results first
    python scripts/predict_fixtures.py --all            # all remaining group games
    python scripts/predict_fixtures.py --plot           # also save heatmaps
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data, elo, matrix as mx  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

RESULTS_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
WC_TOURNAMENT = "FIFA World Cup"


def refresh_snapshot() -> None:
    """Re-download the results snapshot so new results feed current Elo."""
    print(f"Refreshing snapshot from {RESULTS_URL} ...")
    urllib.request.urlretrieve(RESULTS_URL, data.RAW_RESULTS)
    print(f"  wrote {data.RAW_RESULTS.relative_to(data.ROOT)}")


def load_schedule() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (played, upcoming_wc) frames with normalized team names."""
    raw = pd.read_csv(data.RAW_RESULTS)
    raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
    raw = raw.dropna(subset=["date"])
    raw["home_team"] = raw["home_team"].map(data.normalize_team)
    raw["away_team"] = raw["away_team"].map(data.normalize_team)
    if raw["neutral"].dtype == object:
        raw["neutral"] = raw["neutral"].astype(str).str.upper().map(
            {"TRUE": True, "FALSE": False}
        )
    raw["neutral"] = raw["neutral"].astype(bool)

    played = raw.dropna(subset=["home_score", "away_score"]).copy()
    upcoming = raw[
        (raw["tournament"] == WC_TOURNAMENT) & (raw["home_score"].isna())
    ].sort_values("date", kind="mergesort").reset_index(drop=True)
    return played, upcoming


def next_round(upcoming: pd.DataFrame) -> pd.DataFrame:
    """Each team's next unplayed match: greedy over date order.

    A match is included iff neither team has already been claimed by an earlier
    match. On a full group stage this returns exactly the next matchday.
    """
    seen: set[str] = set()
    keep = []
    for fx in upcoming.itertuples(index=False):
        if fx.home_team in seen or fx.away_team in seen:
            continue
        keep.append(fx)
        seen.update([fx.home_team, fx.away_team])
    return pd.DataFrame(keep)


def current_ratings(played: pd.DataFrame) -> tuple[pd.Series, pd.Timestamp]:
    elo_long = elo.compute_elo(played.sort_values("date", kind="mergesort"))
    as_of = played["date"].max()
    return elo.latest_ratings(elo_long, as_of + pd.Timedelta(days=1)), as_of


def main() -> None:
    ap = argparse.ArgumentParser(description="2026 group-stage predictions from current Elo.")
    ap.add_argument("--all", action="store_true",
                    help="predict all remaining group games (default: each team's next match)")
    ap.add_argument("--refresh", action="store_true", help="re-download the results snapshot first")
    ap.add_argument("--model", default=str(data.PROCESSED / "model.json"))
    ap.add_argument("--out", default=str(data.ROOT / "reports" / "wc2026_predictions.csv"))
    ap.add_argument("--plot", action="store_true", help="save a heatmap PNG per fixture")
    args = ap.parse_args()

    if args.refresh:
        refresh_snapshot()

    model = FittedModel.load(args.model)
    played, upcoming = load_schedule()
    if upcoming.empty:
        raise SystemExit("No upcoming FIFA World Cup fixtures in the snapshot.")

    fixtures = upcoming if args.all else next_round(upcoming)
    snap, as_of = current_ratings(played)

    label = "all remaining group games" if args.all else "each team's next match"
    print(f"\n2026 World Cup — {label}  ({len(fixtures)} fixtures)")
    print(f"Elo current as of {as_of:%Y-%m-%d}; model coeffs frozen 2022-11-19.\n")

    rows = []
    for fx in fixtures.itertuples(index=False):
        h, a, neutral = fx.home_team, fx.away_team, bool(fx.neutral)
        if h not in snap.index or a not in snap.index:
            continue
        lam, mu = model.fixture_lambdas(snap, h, a, neutral=neutral)
        M = mx.score_matrix(lam, mu, model.rho)
        d = mx.derived_markets(M)
        (ms_h, ms_a), _ = d["top5_scores"][0]
        rows.append({
            "date": fx.date, "home_team": h, "away_team": a,
            "venue": "neutral" if neutral else f"{h} home",
            "lambda_home": round(lam, 2), "lambda_away": round(mu, 2),
            "p_home": round(d["p_home"], 3), "p_draw": round(d["p_draw"], 3),
            "p_away": round(d["p_away"], 3), "p_over_2_5": round(d["p_over_2_5"], 3),
            "btts_yes": round(d["btts_yes"], 3),
            "top_score": f"{ms_h}-{ms_a}",
            "top3": "; ".join(f"{i}-{j} ({p*100:.0f}%)" for (i, j), p in d["top5_scores"][:3]),
        })

        if args.plot:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig_dir = data.ROOT / "reports" / "figures" / "wc2026"
            fig_dir.mkdir(parents=True, exist_ok=True)
            _, ax = plt.subplots(figsize=(6.5, 6))
            mx.render_matrix(M, h, a, lam, mu, ax=ax)
            plt.tight_layout()
            plt.savefig(fig_dir / f"{fx.date:%m%d}_{h}_{a}.png".replace(" ", "_"), dpi=110)
            plt.close()

    out = pd.DataFrame(rows)
    # Pretty console table.
    hdr = f"{'Date':<7}{'Match':<35}{'Venue':<9}{'λ H/A':<12}{'H / D / A':<19}{'O2.5':<6}{'Top':<5}"
    print(hdr)
    print("-" * len(hdr))
    for r in out.itertuples(index=False):
        venue = "neutral" if r.venue == "neutral" else "host"
        match = f"{r.home_team} v {r.away_team}"[:34]
        print(f"{r.date:%b %d} {match:<35}{venue:<9}"
              f"{f'{r.lambda_home}/{r.lambda_away}':<12}"
              f"{f'{r.p_home:.2f}/{r.p_draw:.2f}/{r.p_away:.2f}':<19}{r.p_over_2_5:<6.2f}{r.top_score:<5}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(f"\nWrote {Path(args.out).relative_to(data.ROOT)}"
          + (f" + heatmaps in reports/figures/wc2026/" if args.plot else ""))
    print("Update loop: once these are played, re-run with --refresh for the next matchday.")


if __name__ == "__main__":
    main()
