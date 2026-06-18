#!/usr/bin/env python3
"""Predict a single fixture from **current** Elo (no freeze).

Computes Elo over every played match in the dataset (current as of the snapshot
date) and applies the fitted Dixon-Coles model to one fixture, printing the
score matrix, 1X2 / O-U 2.5 / BTTS markets, and the top-5 exact scores.

The model *coefficients* come from the frozen 2022-11-19 fit
(`data/processed/model.json`) — they are stable and validated by the backtest —
while the *ratings* are current, so this is a genuine forward prediction.

Examples:
    python scripts/predict_match.py 'Mexico' 'South Africa' --home Mexico
    python scripts/predict_match.py 'Brazil' 'Argentina'          # neutral venue
    python scripts/predict_match.py 'England' 'France' --home England --plot out.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data, elo, matrix as mx  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

MAX_DISPLAY = 6  # show the 0..6 corner of the 9x9 grid in the terminal


def current_ratings():
    """Latest Elo for every team, computed from all played matches (no freeze)."""
    raw = data.load_raw()
    elo_long = elo.compute_elo(raw)
    as_of = raw["date"].max()
    snap = elo.latest_ratings(elo_long, as_of + pd.Timedelta(days=1))
    return snap, as_of


def _resolve_orientation(team1, team2, home):
    """Return (home_team, away_team, neutral) honoring an optional --home side."""
    if home is None:
        return team1, team2, True  # neutral; team1 is just the row axis
    if home not in (team1, team2):
        raise SystemExit(f"--home '{home}' must be one of: '{team1}', '{team2}'")
    away = team2 if home == team1 else team1
    return home, away, False


def _print_matrix(M, home, away, d=MAX_DISPLAY):
    header = "      " + "".join(f"{j:>7}" for j in range(d + 1))
    print(f"\nScore matrix  (rows = {home} goals, cols = {away} goals)  %")
    print(header)
    for i in range(d + 1):
        row = "".join(f"{M[i, j]*100:>7.1f}" for j in range(d + 1))
        print(f"{i:>4}  {row}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Predict a fixture from current Elo.")
    ap.add_argument("team1")
    ap.add_argument("team2")
    ap.add_argument("--home", default=None,
                    help="which side is home (gets home advantage). Omit for a neutral venue.")
    ap.add_argument("--model", default=str(data.forward_model_path()),
                    help="fitted model JSON (default: forward model v2 if built, else v1)")
    ap.add_argument("--plot", default=None, help="optional path to save a heatmap PNG")
    args = ap.parse_args()

    model = FittedModel.load(args.model)
    snap, as_of = current_ratings()

    for name in (args.team1, args.team2):
        if name not in snap.index:
            close = [t for t in snap.index if name.lower() in t.lower()]
            hint = f"  Did you mean: {close[:5]}?" if close else ""
            raise SystemExit(f"Unknown team '{name}'.{hint}")

    home, away, neutral = _resolve_orientation(args.team1, args.team2, args.home)
    lam, mu = model.fixture_lambdas(snap, home, away, neutral=neutral)
    M = mx.score_matrix(lam, mu, model.rho)
    d = mx.derived_markets(M)

    venue = "neutral venue" if neutral else f"{home} at home"
    print(f"\n{home}  vs  {away}   ({venue})")
    print(f"Elo (current, as of {as_of:%Y-%m-%d}): {home} {snap[home]:.0f} | {away} {snap[away]:.0f}")
    print(f"Expected goals (λ): {home} {lam:.2f} | {away} {mu:.2f}")

    _print_matrix(M, home, away)

    print(f"\n1X2:  {home} win {d['p_home']*100:.1f}%  |  draw {d['p_draw']*100:.1f}%  "
          f"|  {away} win {d['p_away']*100:.1f}%")
    print(f"Over 2.5: {d['p_over_2_5']*100:.1f}%  |  Under 2.5: {d['p_under_2_5']*100:.1f}%  "
          f"|  BTTS: {d['btts_yes']*100:.1f}%")
    print("Top 5 exact scores:")
    for (i, j), p in d["top5_scores"]:
        print(f"  {home} {i}-{j} {away}   {p*100:.1f}%")

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        _, ax = plt.subplots(figsize=(6.5, 6))
        mx.render_matrix(M, home, away, lam, mu, ax=ax)
        plt.tight_layout()
        plt.savefig(args.plot, dpi=120)
        print(f"\nSaved heatmap -> {args.plot}")


if __name__ == "__main__":
    main()
