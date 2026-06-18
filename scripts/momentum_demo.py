#!/usr/bin/env python3
"""Show base vs momentum-adjusted predictions for three specific games.

Demonstrates the experimental Elo momentum/form layer on:
  * Mexico v South Africa      (played 2-0)
  * South Korea v Czech Republic (played 2-1)
  * Canada v Bosnia and Herzegovina (upcoming)

Each game is evaluated with ratings as of its own date, comparing the base model
to the same model with the momentum bonus added. Momentum is NOT wired into the
live pipeline — it needs the 2018/2022 backtest gate first.

    python scripts/momentum_demo.py [--alpha 0.5] [--half-life 270]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data, elo, matrix as mx  # noqa: E402
from wcmodel.forward import load_schedule  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

GAMES = [
    ("Mexico", "South Africa", "2026-06-11", False, "2-0"),
    ("South Korea", "Czech Republic", "2026-06-11", True, "2-1"),
    ("Canada", "Bosnia and Herzegovina", "2026-06-12", False, None),
]


def _line(model, ratings, home, away, neutral):
    lam, mu = model.fixture_lambdas(ratings, home, away, neutral=neutral)
    M = mx.score_matrix(lam, mu, model.rho)
    d = mx.derived_markets(M)
    top3 = ", ".join(f"{i}-{j} {p*100:.0f}%" for (i, j), p in d["top5_scores"][:3])
    return lam, mu, d["p_home"], d["p_draw"], d["p_away"], top3


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--half-life", type=float, default=270.0)
    ap.add_argument("--cap", type=float, default=60.0)
    args = ap.parse_args()

    model = FittedModel.load(data.forward_model_path())
    played, _ = load_schedule()
    elo_long = elo.compute_elo(played.sort_values("date", kind="mergesort"))
    mk = dict(alpha=args.alpha, half_life_days=args.half_life, cap=args.cap)

    print(f"Momentum demo  (alpha={args.alpha}, half-life={args.half_life:.0f}d, "
          f"cap=±{args.cap:.0f})\n")
    for home, away, date_s, neutral, actual in GAMES:
        as_of = pd.Timestamp(date_s)
        base = elo.latest_ratings(elo_long, as_of)
        bonus = elo.momentum(elo_long, as_of, **mk)
        eff = base.add(bonus.reindex(base.index).fillna(0.0))

        bh, ba = bonus.get(home, 0.0), bonus.get(away, 0.0)
        head = f"{home} v {away}  ({'neutral' if neutral else home + ' home'}, {date_s})"
        if actual:
            head += f"   actual {actual}"
        print(head)
        print(f"  Elo {home} {base[home]:.0f} (form {bh:+.0f}) | "
              f"{away} {base[away]:.0f} (form {ba:+.0f})")

        lam0, mu0, ph0, pd0, pa0, t0 = _line(model, base, home, away, neutral)
        lam1, mu1, ph1, pd1, pa1, t1 = _line(model, eff, home, away, neutral)
        print(f"  base      λ {lam0:.2f}-{mu0:.2f} | "
              f"{home} {ph0*100:.0f}% / draw {pd0*100:.0f}% / {away} {pa0*100:.0f}%  | top: {t0}")
        print(f"  +momentum λ {lam1:.2f}-{mu1:.2f} | "
              f"{home} {ph1*100:.0f}% / draw {pd1*100:.0f}% / {away} {pa1*100:.0f}%  | top: {t1}")
        print(f"  → 1X2 shift on {home}: {(ph1-ph0)*100:+.1f} pp\n")


if __name__ == "__main__":
    main()
