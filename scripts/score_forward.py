#!/usr/bin/env python3
"""Score the forward log on the **exact-score goal** (and 1X2), live.

Reads ``data/external/wc2026_forward_log.csv`` (predictions + backfilled
results), grades every completed match, and prints a scorecard led by the
exact-score hit rate — the project's primary objective. Writes:

* ``reports/wc2026_forward_scored.csv``  — per-match scored detail
* ``reports/wc2026_forward_metrics.csv`` — one summary row per completion count
  (idempotent: re-running with the same number of completed games overwrites it),
  so the matchday-by-matchday progression accumulates cleanly.

    python scripts/score_forward.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import backtest as bt, data  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

LOG = data.DATA / "external" / "wc2026_forward_log.csv"
SCORED = data.ROOT / "reports" / "wc2026_forward_scored.csv"
METRICS = data.ROOT / "reports" / "wc2026_forward_metrics.csv"


def main() -> None:
    if not LOG.exists():
        raise SystemExit(f"No forward log at {LOG}")
    log = pd.read_csv(LOG)
    model = FittedModel.load(data.forward_model_path())
    s = bt.score_forward_log(log, model.rho)
    if s["n"] == 0:
        print("No completed matches in the forward log yet.")
        return

    n = s["n"]
    print("=" * 60)
    print(f"FORWARD SCORECARD — {n} completed match(es)")
    print("=" * 60)
    print("\n🎯 EXACT SCORE (primary goal)")
    print(f"   Exact hits (our pick == result):  {s['exact']}/{n}  ({s['exact']/n*100:.0f}%)")
    print(f"   Result in our top-3 scorelines:   {s['top3']}/{n}  ({s['top3']/n*100:.0f}%)")
    print(f"   Result in our top-5 scorelines:   {s['top5']}/{n}  ({s['top5']/n*100:.0f}%)")
    print(f"   Top pick within 1 goal each side: {s['within1']}/{n}  ({s['within1']/n*100:.0f}%)")
    print("\n📊 1X2 / probabilistic")
    print(f"   Directional (winner) hits:        {s['dir']}/{n}  ({s['dir']/n*100:.0f}%)")
    print(f"   Model RPS:                        {s['rps']:.4f}")
    if s["n_mkt"]:
        lead = "model ahead" if s["mkt_rps_model"] < s["mkt_rps"] else "market ahead"
        print(f"   vs market ({s['n_mkt']} priced):       model {s['mkt_rps_model']:.4f} / market {s['mkt_rps']:.4f} ({lead})")
    print(f"   Exact-score log loss:             {s['logloss']:.4f}")
    print("\n⚽ GOALS vs MODEL xG")
    print(f"   Actual goals:   {s['goals_actual']}   |   model xG: {s['xg']:.1f}   |   bias: {s['goals_actual']-s['xg']:+.1f}")

    s["per_match"].to_csv(SCORED, index=False)

    summary = {
        "n_completed": n, "exact": s["exact"], "top3": s["top3"], "top5": s["top5"],
        "within1": s["within1"], "dir": s["dir"], "rps": round(s["rps"], 4),
        "mkt_rps": round(s["mkt_rps"], 4) if s["n_mkt"] else None,
        "logloss": round(s["logloss"], 4),
        "goals_actual": s["goals_actual"], "xg": round(s["xg"], 1),
    }
    hist = pd.read_csv(METRICS) if METRICS.exists() else pd.DataFrame(columns=list(summary))
    hist = hist[hist["n_completed"] != n]  # idempotent upsert on completion count
    hist = pd.concat([hist, pd.DataFrame([summary])], ignore_index=True).sort_values("n_completed")
    hist.to_csv(METRICS, index=False)
    print(f"\nWrote {SCORED.relative_to(data.ROOT)} and {METRICS.relative_to(data.ROOT)}")


if __name__ == "__main__":
    main()
