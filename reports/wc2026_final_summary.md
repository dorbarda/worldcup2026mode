# World Cup 2026 — Final Forward-Test Summary

101 completed matches scored, 2026-06-11 (opening matchday) → 2026-07-18
(final). Auto-scored detail in [`wc2026_forward_scored.csv`](wc2026_forward_scored.csv),
matchday-by-matchday progression in [`wc2026_forward_metrics.csv`](wc2026_forward_metrics.csv).
Model: Dixon-Coles Poisson (`v2`, goal_scale=1.10), coefficients frozen at the
2022-11-19 backtest fit; only Elo ratings moved forward.

## Headline scorecard (all 101 matches)

| Metric | Hits | Rate |
|---|---|---|
| **Exact score** (primary goal) | 13/101 | 13% |
| Result in top-3 scorelines | 35/101 | 35% |
| Result in top-5 scorelines | 52/101 | 51% |
| Top pick within 1 goal each side | 62/101 | 61% |
| **Directional (1X2) winner** | 65/101 | 64% |
| Model RPS (lower=better) | — | 0.1621 |
| Exact-score log loss | — | 2.972 |

## vs. the betting market (98 priced fixtures)

| | RPS |
|---|---|
| Model | 0.1597 |
| Market (de-vigged) | 0.1450 |

**Market ahead.** Consistent with the pre-tournament read in
[`odds_integration_decision.md`](odds_integration_decision.md) — the PRD never
expected to beat the market, and the model was kept as a comparison layer, not
blended in, precisely because this was the likely outcome.

## Group stage vs. knockouts — the model got *better* as the field thinned

| Metric | Group stage (72) | Knockouts (29) |
|---|---|---|
| Exact score | 7/72 (10%) | 6/29 (21%) |
| Top-3 | 24/72 (33%) | 11/29 (38%) |
| Top-5 | 33/72 (46%) | 19/29 (66%) |
| Within 1 goal | 40/72 (56%) | 22/29 (76%) |
| Directional | 41/72 (57%) | 24/29 (83%) |
| RPS | 0.168 | 0.148 |

Once the 48-team field is down to knockout survivors, matchups skew toward
clearer favourites (fewer 60-seed-vs-2-seed upset traps than the group stage),
and the model's Elo-driven confidence pays off — directional accuracy jumps
from 57% to 83%.

## What worked

- **Directional calls (64% overall, 83% in knockouts)** were the strongest
  signal — the Elo + Dixon-Coles core does what it was built for: ranking two
  teams correctly more often than not.
- **Top-5 coverage (51%)** and **within-1-goal (61%)** show the model is
  usually in the right neighborhood even when it misses the exact score.
- Knockout-stage calibration held up notably better than group stage across
  every metric.
- The exact-score hit rate (13%) beat the PRD's own backtest expectation band
  (5–7/48 ≈ 10–15%, calibrated on Qatar 2022/Russia 2018) — in range, arguably
  slightly ahead of historical norms.

## What didn't work

- **Goals under-prediction, badly.** Actual goals 301 vs model xG 256.1 —
  a **+44.9 bias (+17.5%)**, worse than the ~10.5% gap the v2 `goal_scale=1.10`
  patch was calibrated to close pre-tournament. The single biggest driver: a
  cluster of blowouts the model never assigns real mass to —
  Germany 7-1 Curaçao, Sweden 5-1 Tunisia, England 4-2 Croatia, Netherlands
  5-1 Sweden, New Zealand 1-5 Belgium, Morocco 4-2 Haiti — plus the wild
  France 4-6 England final, the single worst call of the tournament
  (log loss 10.8, actual 10 goals vs 2.3 xG). This is the same "model
  under-predicts blowouts" weakness flagged in the pre-tournament README from
  the Qatar 2022 / Russia 2018 backtests (England 6-2 Iran, Spain 7-0 Costa
  Rica) — it carried straight through into the live tournament, unresolved.
- **Lost to the market** on RPS (0.160 vs 0.145 on priced fixtures) — expected
  going in, per the odds-integration decision, but confirms the model alone
  isn't priced as sharply as the book.
- **Group stage was the weak link.** Every metric (exact, top-3, directional,
  RPS) was worse in the group stage than knockouts — the expanded 48-team
  format's group stage carries more mismatched/upset-prone fixtures than a
  32-team bracket, and the flat Elo/home-advantage model doesn't capture
  team-specific host effects or motivation (a pattern already surfaced on
  matchday 1 in the odds-disagreement diagnostic: Canada/Mexico/USA host
  calibration was off, and favourites were "compressed" relative to market
  confidence on Brazil, Netherlands, France).

## Bottom line

The model did what a frozen, leakage-free, coefficients-never-touched Poisson
model can reasonably do: called the winner right about two-thirds of the time
(better than that in the business end of the tournament), landed the exact
score about 1 in 8 times, but systematically undersold how many goals actual
World Cup matches produce — and, as expected, didn't out-price the betting
market. No model changes were made mid-tournament (by design — the PRD's
zero-leakage, frozen-coefficients principle held for the full run).
