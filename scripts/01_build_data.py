#!/usr/bin/env python3
"""M1 + M2: build the cleaned data, the test-set quarantine, and Elo history.

Reads ``data/raw/results.csv`` and writes, for a given **freeze date**:

* ``<proc>/elo_history.parquet``  — (date, team, rating_pre/post_match)
* ``<proc>/team_match.parquet``   — long team-match rows + as-of Elo
* (for a tournament freeze) ``data/test/<key>_group_stage.csv`` — 48 fixtures

Two ways to choose the freeze:

* **Backtest (default):** a tournament key picks its frozen cutoff.
  ``python scripts/01_build_data.py [qatar2022|russia2018]``  (default qatar2022,
  i.e. freeze 2022-11-19) → writes to the canonical ``data/processed/``.

* **Forward / current:** an explicit ``--freeze-date`` rebuilds Elo + team_match
  up to any date (e.g. today) for live prediction.
  ``python scripts/01_build_data.py --freeze-date 2026-06-10``
  → writes to ``data/processed/asof_2026-06-10/`` so the **frozen backtest
  artifacts in ``data/processed/`` are never touched.**
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data, elo  # noqa: E402


def build(raw, freeze, proc_dir, label, test=None, test_path=None) -> None:
    """Build Elo + team_match frozen at ``freeze`` into ``proc_dir``."""
    proc_dir.mkdir(parents=True, exist_ok=True)
    print(f"=== Building data frozen at {freeze:%Y-%m-%d} ({label}) ===")
    print(f"  raw: {len(raw):,} played matches, "
          f"{raw.date.min():%Y-%m-%d} -> {raw.date.max():%Y-%m-%d}")

    # --- Test-set quarantine (tournament builds only) ----------------------- #
    if test is not None:
        test_path.parent.mkdir(parents=True, exist_ok=True)
        test.to_csv(test_path, index=False)
        assert len(test) == 48, f"expected 48 group-stage matches, got {len(test)}"
        print(f"Wrote test set: {len(test)} matches -> {test_path.relative_to(data.ROOT)}")

    # --- Elo over history up to the freeze (leakage guard) ------------------- #
    train = raw.loc[raw["date"] <= freeze].reset_index(drop=True)
    assert train["date"].max() <= freeze, "leakage: training rows after freeze"
    print(f"Training matches (<= {freeze:%Y-%m-%d}): {len(train):,}")

    print("Computing Elo ...")
    elo_long = elo.compute_elo(train)

    hist = elo.elo_history(elo_long)
    hist.to_parquet(proc_dir / "elo_history.parquet", index=False)
    print(f"Wrote elo_history: {len(hist):,} rows -> "
          f"{(proc_dir / 'elo_history.parquet').relative_to(data.ROOT)}")

    team_match = elo_long.loc[elo_long["date"] >= data.FEATURE_START].reset_index(drop=True)
    team_match.to_parquet(proc_dir / "team_match.parquet", index=False)
    print(f"Wrote team_match: {len(team_match):,} rows (>= {data.FEATURE_START:%Y-%m-%d}) -> "
          f"{(proc_dir / 'team_match.parquet').relative_to(data.ROOT)}")

    snap = elo.latest_ratings(elo_long, freeze + pd.Timedelta(days=1)).sort_values(ascending=False)
    print(f"\nTop 10 by Elo at {freeze:%Y-%m-%d}:")
    for team, r in snap.head(10).items():
        print(f"  {team:<18} {r:7.1f}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build data + Elo frozen at a date.")
    ap.add_argument("tournament", nargs="?", default="qatar2022",
                    choices=sorted(data.TOURNAMENTS), help="backtest tournament (default qatar2022)")
    ap.add_argument("--freeze-date", default=None,
                    help="override: build Elo/team_match up to this YYYY-MM-DD "
                         "(default: the tournament's frozen cutoff, 2022-11-19 for qatar2022). "
                         "Non-default dates write to data/processed/asof_<date>/.")
    args = ap.parse_args()

    raw = data.load_raw()
    t = data.TOURNAMENTS[args.tournament]

    if args.freeze_date is None:
        # Backtest build: tournament cutoff, canonical/namespaced proc dir + test set.
        build(raw, t.freeze, t.proc_dir, t.name,
              test=data.extract_test_set(raw, t), test_path=t.test_path)
    else:
        freeze = pd.Timestamp(args.freeze_date)
        proc = data.asof_proc_dir(freeze)
        if freeze == t.freeze:
            # Same cutoff as the tournament -> also emit its test set.
            build(raw, freeze, proc, f"{t.name} freeze",
                  test=data.extract_test_set(raw, t), test_path=t.test_path)
        else:
            build(raw, freeze, proc, f"as-of {freeze:%Y-%m-%d}")


if __name__ == "__main__":
    main()
