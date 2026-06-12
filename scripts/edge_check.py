#!/usr/bin/env python3
"""Investigate upcoming games where our model disagrees a lot with the market.

For every upcoming fixture with odds, compute the biggest gap between our 1X2 and
the de-vigged market. For games over the threshold (default 15pp), run three
checks to help you decide whether the disagreement is a real edge or a model
blind spot:

  1) Home/host?  — hosts are a known over/under-rating spot for the model.
  2) Injuries    — the model is blind to squad news; YOU check and confirm.
  3) Momentum    — what changes if we crank form up; does it move us toward the
                   market (so recent form might explain the gap) or not?

This is a decision-support tool — it does NOT change the model.

    python scripts/edge_check.py [--threshold 0.15] [--alpha 4] [--all]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data, elo, matrix as mx, odds  # noqa: E402
from wcmodel.forward import load_schedule, next_round  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

OUTCOMES = ["home", "draw", "away"]


def _probs(model, ratings, h, a, neutral):
    lam, mu = model.fixture_lambdas(ratings, h, a, neutral=neutral)
    d = mx.derived_markets(mx.score_matrix(lam, mu, model.rho))
    return np.array([d["p_home"], d["p_draw"], d["p_away"]])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.15, help="flag |our-market| >= this (default 0.15)")
    ap.add_argument("--alpha", type=float, default=2.0, help="'strong' momentum strength for check 3")
    ap.add_argument("--all", action="store_true", help="scan all upcoming games (default: next matchday)")
    args = ap.parse_args()

    model = FittedModel.load(data.PROCESSED / "model.json")
    played, upcoming = load_schedule()
    fixtures = upcoming if args.all else next_round(upcoming)
    elo_long = elo.compute_elo(played.sort_values("date", kind="mergesort"))
    as_of = played["date"].max() + pd.Timedelta(days=1)
    base = elo.latest_ratings(elo_long, as_of)
    # High cap so "strong momentum" differentiates teams by recent form instead
    # of everyone saturating the same ceiling.
    bonus = elo.momentum(elo_long, as_of, alpha=args.alpha, half_life_days=270, cap=120)
    eff = base.add(bonus.reindex(base.index).fillna(0.0))

    devig = odds.load_market(fixtures)
    if devig is None:
        raise SystemExit("No market odds available to compare against.")

    flagged = []
    for i, fx in enumerate(fixtures.itertuples(index=False)):
        h, a, neutral = fx.home_team, fx.away_team, bool(fx.neutral)
        if h not in base.index or a not in base.index or np.isnan(devig[i]).all():
            continue
        ours = _probs(model, base, h, a, neutral)
        edge = float(np.max(np.abs(ours - devig[i])))
        if edge >= args.threshold:
            flagged.append((edge, i, fx, h, a, neutral, ours, devig[i]))
    flagged.sort(reverse=True, key=lambda t: t[0])

    print(f"\nEdge check — {len(flagged)} game(s) with |model − market| ≥ "
          f"{args.threshold*100:.0f}pp  (strong-momentum α={args.alpha})\n")
    if not flagged:
        print("No major disagreements right now.")
        return

    for edge, i, fx, h, a, neutral, ours, mkt in flagged:
        # The outcome we disagree on most.
        k = int(np.argmax(np.abs(ours - mkt)))
        side = OUTCOMES[k]
        higher = ours[k] > mkt[k]
        print(f"=== {h} v {a}  ({fx.date:%a %b %d}) — edge {edge*100:.0f}pp ===")
        print(f"    ours {ours[0]*100:.0f}/{ours[1]*100:.0f}/{ours[2]*100:.0f}  "
              f"vs market {mkt[0]*100:.0f}/{mkt[1]*100:.0f}/{mkt[2]*100:.0f}  "
              f"(we're {'higher' if higher else 'lower'} on {side})")

        # 1) Home/host — compare our vs market view of the host specifically.
        if neutral:
            print("  1) Venue: neutral — not a host effect.")
        else:
            if ours[0] > mkt[0] + 0.05:
                note = "we're HIGHER on the host than the market — classic host-OVERrating spot"
            elif ours[0] < mkt[0] - 0.05:
                note = "we're LOWER on the host than the market — host-UNDERrating (USA-style)"
            else:
                note = "our host view roughly matches the market"
            print(f"  1) Venue: {h} at HOME — {note}.")

        # 2) Injuries (human in the loop)
        print(f"  2) Injuries: 🔍 CHECK squad news for {h} and {a} "
              f"(suspensions/injuries/rotation) — the model can't see these.")

        # 3) Momentum
        ours_m = _probs(model, eff, h, a, neutral)
        new_edge = float(np.max(np.abs(ours_m - mkt)))
        bh, ba = bonus.get(h, 0.0), bonus.get(a, 0.0)
        direction = ("moves us TOWARD the market" if new_edge < edge - 0.02
                     else "moves us AWAY from the market" if new_edge > edge + 0.02
                     else "barely changes it")
        print(f"  3) Strong momentum: ours → {ours_m[0]*100:.0f}/{ours_m[1]*100:.0f}/{ours_m[2]*100:.0f} "
              f"(form {h} {bh:+.0f}, {a} {ba:+.0f}) — {direction} "
              f"(edge {edge*100:.0f}→{new_edge*100:.0f}pp).")
        if new_edge < edge - 0.02:
            print("     ↳ recent form may explain part of the gap.")
        print()


if __name__ == "__main__":
    main()
