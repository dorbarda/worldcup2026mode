#!/usr/bin/env python3
"""M1 + M2: build the cleaned data, the test-set quarantine, and Elo history.

Reads ``data/raw/results.csv`` and writes:

* ``data/test/qatar2022_group_stage.csv`` — 48 group fixtures + actual results
* ``data/processed/elo_history.parquet``  — (date, team, rating_pre/post_match)
* ``data/processed/team_match.parquet``   — long team-match rows + as-of Elo,
                                             frozen at the training cutoff

Usage: ``python scripts/01_build_data.py [tournament_key]``  (default qatar2022)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data, elo  # noqa: E402


def main(t: data.Tournament = data.QATAR2022) -> None:
    t.proc_dir.mkdir(parents=True, exist_ok=True)
    t.test_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"=== Building data frozen for {t.name} (freeze {t.freeze:%Y-%m-%d}) ===")

    print("Loading raw results ...")
    raw = data.load_raw()
    print(f"  {len(raw):,} played matches, {raw.date.min():%Y-%m-%d} -> {raw.date.max():%Y-%m-%d}")

    # --- Test-set quarantine ------------------------------------------------ #
    test = data.extract_test_set(raw, t)
    test.to_csv(t.test_path, index=False)
    print(f"Wrote test set: {len(test)} matches -> {t.test_path.relative_to(data.ROOT)}")
    assert len(test) == 48, f"expected 48 group-stage matches, got {len(test)}"

    # --- Elo over the full history (training portion only) ------------------ #
    train = data.training_frame(raw, t)
    data.assert_no_leakage(train, t)
    print(f"Training matches (<= freeze {t.freeze:%Y-%m-%d}): {len(train):,}")

    print("Computing Elo ...")
    elo_long = elo.compute_elo(train)

    hist = elo.elo_history(elo_long)
    hist.to_parquet(t.proc_dir / "elo_history.parquet", index=False)
    print(f"Wrote elo_history: {len(hist):,} rows -> {(t.proc_dir / 'elo_history.parquet').relative_to(data.ROOT)}")

    # --- Model training table (feature era only) ---------------------------- #
    team_match = elo_long.loc[elo_long["date"] >= data.FEATURE_START].reset_index(drop=True)
    team_match.to_parquet(t.proc_dir / "team_match.parquet", index=False)
    print(
        f"Wrote team_match: {len(team_match):,} rows "
        f"(>= {data.FEATURE_START:%Y-%m-%d}) -> {(t.proc_dir / 'team_match.parquet').relative_to(data.ROOT)}"
    )

    # --- Spot-check: a few teams' ratings as of the freeze ------------------ #
    snap = elo.latest_ratings(elo_long, t.freeze).sort_values(ascending=False)
    print(f"\nTop 10 by Elo at freeze ({t.freeze:%Y-%m-%d}):")
    for team, r in snap.head(10).items():
        print(f"  {team:<18} {r:7.1f}")


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "qatar2022"
    main(data.TOURNAMENTS[key])
