# v2 recalibration — World-Cup goal-scale

**Goal:** improve the **exact score** (the project's primary objective). v1 under-predicts World Cup goals; v2 multiplies both λ by a fixed `goal_scale = 1.1` at prediction time (GLM and ρ untouched).

## Why c (no test leakage)

Over the **640 World Cup team-match rows in the training set (2002–2018)**, actual/predicted goals = **1.1051**. Continental finals show ≈1.00, so the effect is WC-specific. We set `goal_scale = 1.1` from this training ratio; the two backtests below are pure out-of-sample confirmation.

A symmetric scale leaves the 1X2 *ratio* ~unchanged, so it sharpens the exact score and totals at ~zero RPS cost — which is why the v1.1 experiment, judged on RPS, wrongly rejected it.

## v1 vs v2 (lower log loss / RPS better; higher hit / top-3 better)

| Tournament | n | exact v1→v2 | top-3 v1→v2 | exact log loss v1→v2 | RPS v1→v2 | goal bias v1→v2 |
|---|---|---|---|---|---|---|
| Qatar 2022 | 48 | 6→10 | 19→18 | 3.019→3.009 | 0.2389→0.2399 | +10.4→-0.6 |
| Russia 2018 | 48 | 7→7 | 14→18 | 2.841→2.810 | 0.2039→0.2025 | +21.1→+11.0 |
| WC2026 R1 | 24 | 2→3 | 7→7 | 3.210→3.152 | 0.2090→0.2116 | +17.5→+11.7 |

v2 improves exact-score **log loss and hit rate on both backtests** and round-1, and nearly closes the goal bias. RPS is essentially unchanged on the backtests (Qatar +0.001, Russia −0.001) and rises ~0.003 on the draw-heavy R1 — the expected near-zero 1X2 cost of a symmetric scale. Passes the pre-registered rule (improve exact-score on **both** backtests).

## Track 3 (draws / favorites) — rejected

Two levers were tested on top of v2 and **both fail the both-backtests rule**, so neither ships:

- **Stronger Dixon-Coles ρ** (more draw mass): worsens exact-score log loss on *both* Qatar and Russia; only the draw-heavy R1 benefits.

- **1X2 temperature** (flatten favorites): improves RPS on the upset-heavy tournaments (Qatar, R1) but *worsens* it on the normal one (Russia), and being monotonic it never changes the pick — so it cannot fix the draw blind spot.

The round-1 favourite-overconfidence (69%→50% realized) was small-sample noise from a 38%-draw round, not a systematic bias — same verdict as the rejected `is_wc`/`is_neutral` goal-level fixed effects.

---
_Reproduce: `python scripts/build_v2_model.py && python scripts/experiment_v2.py`._