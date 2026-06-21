# WC-2026 simulation — last 8 & next 8 group games

*Monte-Carlo, 50,000 draws/match, seed 2026. Generated from `data/external/wc2026_forward_log.csv`.*

## Tweaks applied (fit on the completed games)

- **Level:** raw actual/xG = 1.222; shrunk extra scale = **×1.148** on top of v2's 1.10 (effective ≈ 1.26).
- **Fat tail:** Negative-Binomial dispersion **r = 7.7** (Poisson = ∞), fit by MLE on completed team innings.

## Last 8 games — tweaked model vs actual

| Date | Match | Sim H/D/A | Sim top scores | Sim xG | Actual | P(actual) | In top-3? |
|---|---|---|---|---|---|---|---|
| 2026-06-19 | Scotland v Morocco | 25/24/51 | 0-1 (11%); 1-1 (10%); 0-2 (9%) | 2.71 | **0-1** | 11% | ✓ |
| 2026-06-19 | Brazil v Haiti | 76/15/9 | 2-0 (12%); 1-0 (11%); 3-0 (10%) | 3.32 | **3-0** | 10% | ✓ |
| 2026-06-19 | United States v Australia | 37/24/39 | 1-1 (10%); 0-1 (8%); 1-0 (8%) | 3.01 | **2-0** | 6% | · |
| 2026-06-19 | Turkey v Paraguay | 43/25/32 | 1-1 (11%); 1-0 (10%); 0-1 (9%) | 2.67 | **0-1** | 9% | ✓ |
| 2026-06-20 | Netherlands v Sweden | 58/22/20 | 1-0 (12%); 2-0 (10%); 1-1 (10%) | 2.82 | **5-1** | 1% | · |
| 2026-06-20 | Germany v Ivory Coast | 55/23/22 | 1-0 (11%); 1-1 (10%); 2-0 (10%) | 2.76 | **2-1** | 8% | · |
| 2026-06-20 | Ecuador v Curaçao | 78/14/8 | 2-0 (12%); 1-0 (10%); 3-0 (10%) | 3.38 | **0-0** | 5% | · |
| 2026-06-20 | Tunisia v Japan | 11/17/72 | 0-2 (12%); 0-1 (11%); 0-3 (9%) | 3.13 | **0-4** | 6% | · |

Actual scoreline inside the simulated top-3: **3/8**.

**Did the tweaks help on these 8?** Summed goal expectation vs the 20 goals actually scored: base v2 = 20.7 (bias +0.7) → tweaked = 23.8 (bias +3.8). Note these particular 8 were a *low-scoring* batch (2.50/match, right at the historical norm), so the level tweak — fit on the full 36-game +22% excess — overshoots *here*. That's the whole reason the scale is shrunk and meant to re-fit as games accrue, not chase any single matchday. The fat-tail tweak is the unambiguous win: it gives the blowouts (5-1, 0-4) realistic probability mass that Poisson rated near-impossible, independent of the level.

## Next 8 games — simulated forecast

| Date | Match | H/D/A | Top scores | Sim xG | Over 2.5 | P(≥4 goals) |
|---|---|---|---|---|---|---|
| 2026-06-21 | Belgium v Iran | 43/25/32 | 1-1 (11%); 1-0 (11%); 0-1 (9%) | 2.65 | 48% | 28% |
| 2026-06-21 | New Zealand v Egypt | 30/25/45 | 1-1 (11%); 0-1 (10%); 1-0 (8%) | 2.70 | 49% | 29% |
| 2026-06-21 | Spain v Saudi Arabia | 86/10/4 | 2-0 (11%); 3-0 (11%); 4-0 (9%) | 3.89 | 70% | 52% |
| 2026-06-21 | Uruguay v Cape Verde | 68/19/13 | 1-0 (12%); 2-0 (11%); 3-0 (8%) | 3.03 | 56% | 36% |
| 2026-06-22 | France v Iraq | 82/12/6 | 2-0 (12%); 3-0 (11%); 1-0 (10%) | 3.62 | 66% | 47% |
| 2026-06-22 | Norway v Senegal | 50/24/26 | 1-0 (11%); 1-1 (10%); 2-0 (9%) | 2.71 | 50% | 29% |
| 2026-06-22 | Argentina v Austria | 69/18/12 | 2-0 (11%); 1-0 (11%); 3-0 (8%) | 3.08 | 57% | 37% |
| 2026-06-22 | Jordan v Algeria | 25/24/51 | 0-1 (11%); 1-1 (10%); 0-2 (9%) | 2.74 | 50% | 30% |
