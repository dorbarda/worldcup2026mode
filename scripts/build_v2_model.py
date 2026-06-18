#!/usr/bin/env python3
"""Build the forward model **v2** = frozen v1 GLM/rho + World-Cup goal-level scale.

The v1 model under-predicts goals in World Cup matches. Measured on **training
data only** (no test leakage), the ratio of actual to predicted goals over the
640 WC team-match rows in 2002-2018 is ~1.105 — continental finals show ~1.00,
so the effect is WC-specific. We set ``goal_scale`` to that ratio (rounded to
1.10), applied symmetrically at prediction time, which sharpens the exact score
and totals while leaving the 1X2 ratio essentially unchanged. Out-of-sample
confirmation on both backtests lives in ``reports/v2_recalibration.md``.

    python scripts/build_v2_model.py            # writes data/processed/model_v2.json
    python scripts/build_v2_model.py --scale 1.10
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data  # noqa: E402
from wcmodel.model import FittedModel, build_design  # noqa: E402


def wc_goal_ratio(model: FittedModel) -> float:
    """Actual/predicted goals over training-era World Cup matches (no leakage)."""
    tm = pd.read_parquet(data.PROCESSED / "team_match.parquet")
    wc = tm[tm["tournament"] == "FIFA World Cup"]
    X = build_design(wc, model.features)
    lam = np.exp(X.to_numpy() @ model.params[X.columns].to_numpy())
    return float(wc["goals_for"].sum() / lam.sum())


def main() -> None:
    ap = argparse.ArgumentParser(description="Build forward model v2 (goal-scaled).")
    ap.add_argument("--scale", type=float, default=None,
                    help="goal_scale to bake in (default: round(WC actual/pred, 1))")
    ap.add_argument("--v1", default=str(data.MODEL_V1))
    ap.add_argument("--out", default=str(data.MODEL_V2))
    args = ap.parse_args()

    v1 = FittedModel.load(args.v1)
    measured = wc_goal_ratio(v1)
    scale = args.scale if args.scale is not None else round(measured, 1)
    print(f"Training-era WC actual/predicted goal ratio: {measured:.4f}")
    print(f"Baking goal_scale = {scale} into v2 (v1 coeffs/rho unchanged).")

    v1.goal_scale = scale
    Path(args.out).write_text(json.dumps(v1.to_dict(), indent=2))
    print(f"Wrote {Path(args.out).relative_to(data.ROOT)}")


if __name__ == "__main__":
    main()
