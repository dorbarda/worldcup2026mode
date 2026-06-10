#!/usr/bin/env python3
"""M1 + M2: build the cleaned data, the test-set quarantine, and Elo history.

Reads ``data/raw/results.csv`` and writes:

* ``data/test/qatar2022_group_stage.csv`` — 48 group fixtures + actual results
* ``data/processed/elo_history.parquet``  — (date, team, rating_pre/post_match)
* ``data/processed/team_match.parquet``   — long team-match rows + as-of Elo,
                                             frozen at the training cutoff

Run from the repo root: ``python scripts/01_build_data.py``
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data, elo  # noqa: E402


def main() -> None:
    data.PROCESSED.mkdir(parents=True, exist_ok=True)
    data.TEST_FIXTURES.parent.mkdir(parents=True, exist_ok=True)

    print("Loading raw results ...")
    raw = data.load_raw()
    print(f"  {len(raw):,} played matches, {raw.date.min():%Y-%m-%d} -> {raw.date.max():%Y-%m-%d}")

    # --- Test-set quarantine ------------------------------------------------ #
    test = data.extract_test_set(raw)
    test.to_csv(data.TEST_FIXTURES, index=False)
    print(f"Wrote test set: {len(test)} matches -> {data.TEST_FIXTURES.relative_to(data.ROOT)}")
    assert len(test) == 48, f"expected 48 group-stage matches, got {len(test)}"

    # --- Elo over the full history (training portion only) ------------------ #
    train = data.training_frame(raw)
    data.assert_no_leakage(train)
    print(f"Training matches (<= freeze {data.FREEZE_DATE:%Y-%m-%d}): {len(train):,}")

    print("Computing Elo ...")
    elo_long = elo.compute_elo(train)

    hist = elo.elo_history(elo_long)
    hist.to_parquet(data.PROCESSED / "elo_history.parquet", index=False)
    print(f"Wrote elo_history: {len(hist):,} rows -> data/processed/elo_history.parquet")

    # --- Model training table (feature era only) ---------------------------- #
    team_match = elo_long.loc[elo_long["date"] >= data.FEATURE_START].reset_index(drop=True)
    team_match.to_parquet(data.PROCESSED / "team_match.parquet", index=False)
    print(
        f"Wrote team_match: {len(team_match):,} rows "
        f"(>= {data.FEATURE_START:%Y-%m-%d}) -> data/processed/team_match.parquet"
    )

    # --- Spot-check: a few teams' ratings as of the freeze ------------------ #
    snap = elo.latest_ratings(elo_long, data.FREEZE_DATE).sort_values(ascending=False)
    print("\nTop 10 by Elo at freeze (2022-11-19):")
    for team, r in snap.head(10).items():
        print(f"  {team:<18} {r:7.1f}")


if __name__ == "__main__":
    main()
