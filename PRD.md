# PRD — World Cup Exact-Score Prediction Model ("Poisson Matrix")

**Owner:** Dor
**Version:** 1.0
**Status:** Ready for implementation
**Target:** Public GitHub repo, built with Claude Code

---

## 1. Overview

Build a reproducible model that predicts the **exact-score probability matrix** for international football matches (style: the classic Poisson score grid — e.g., Mexico 2.10 / South Africa 0.55 expected goals → 8×8 matrix of score probabilities → derived 1X2 / O-U / BTTS markets).

The project has two phases:

1. **Backtest (v1, this PRD):** Train the model on data frozen at **November 19, 2022** and evaluate it against the actual **Qatar 2022 group stage** (48 matches).
2. **Forward (v2, out of scope here):** Point the validated model at World Cup 2026 matches.

**Core principle: zero data leakage.** The model may only see information available before the prediction date. This is enforced in code, not by convention.

---

## 2. Goals & Non-Goals

### Goals
- A fitted Dixon-Coles-style Poisson model producing per-match score matrices
- A rigorous, honest backtest against Qatar 2022 group stage with proper baselines
- Clean, reproducible pipeline: one command from raw data → evaluation report
- Repo quality good enough to share publicly (The Cousins / X audience)

### Non-Goals (v1)
- No xG data (spotty for internationals — v2)
- No player/lineup layer
- No live/in-play modeling
- No betting strategy / Kelly sizing layer (separate project)
- No web UI (CLI + notebook outputs only)

---

## 3. Data

### 3.1 Primary dataset
- **Source:** Kaggle — `martj42/international-football-results-from-1872-to-2017` (maintained, covers through present)
- **File:** `results.csv`
- **Columns used:** `date`, `home_team`, `away_team`, `home_score`, `away_score`, `tournament`, `city`, `country`, `neutral`
- Download once, commit a snapshot to `data/raw/` (it's small, ~10MB) so the repo is fully reproducible without Kaggle credentials. Document the snapshot date in `data/README.md`.

### 3.2 Elo ratings — computed, not scraped
Rebuild Elo from the results dataset rather than scraping eloratings.net. Reasons: reproducibility, and we need **as-of-date** ratings (rating each team had on each match date), which scraping makes painful.

**Elo spec (follow eloratings.net conventions):**
- Start all teams at 1500 (or seed continental tiers if simple to do; flat 1500 is acceptable since we burn in from 1993)
- K-factor by competition: World Cup = 60, continental finals/Confed = 50, WC & continental qualifiers = 40, other tournaments = 30, friendlies = 20
- Goal-difference multiplier: win by 2 → K×1.5, by 3 → K×1.75, by N≥4 → K×(1.75 + (N−3)/8)
- Home advantage: +100 Elo points to home team's rating in expectancy calc, **zero when `neutral == True`**
- Expectancy: `W_e = 1 / (10^(−dr/400) + 1)` where `dr` = rating diff incl. home bonus
- Burn-in: compute Elo from 1993 onward; only use ratings from 2000+ as model features

**Deliverable:** `elo.py` module + `data/processed/elo_history.parquet` with (date, team, rating_pre_match, rating_post_match).

### 3.3 Train/test split (hard freeze)
- **Training window:** 2000-01-01 → 2022-11-19 (inclusive)
- **Test set:** the 48 Qatar 2022 group-stage matches (2022-11-20 → 2022-12-02)
- Store the test fixtures + actual results in a separate file `data/test/qatar2022_group_stage.csv` (build it from the same Kaggle data, but the pipeline must never read actual test scores until the evaluation step)
- Add an automated leakage guard: training code asserts `max(date) <= 2022-11-19`

---

## 4. Model Specification

### 4.1 Goal-expectation model (the λs)
Fit a **Poisson GLM** (log link) on team-match rows (each match = 2 rows, one per team's goals scored):

```
goals_scored ~ elo_diff + is_home + intercept
```

Where:
- `elo_diff` = (team Elo − opponent Elo) / 400, as-of match date, **excluding** the +100 home bonus (home enters as its own term)
- `is_home` = 1 if team is home and `neutral == False`, else 0
- Consider also `elo_sum` or `elo_opponent` as a feature (stronger opponents suppress total goals) — test in EDA, keep if it improves CV log-loss

**Sample weights — multiplicative:**
- Time decay: `w_time = exp(−ξ × days_before_cutoff)`, fit ξ by maximizing out-of-sample log-likelihood on a validation slice (grid: 0.001–0.01 per day; expect ~0.002–0.005, i.e., half-life roughly 6–24 months)
- Competition weight: World Cup/continental = 1.0, qualifiers = 0.9, other tournaments = 0.7, friendlies = 0.5
- COVID flag: down-weight matches 2020-03 → 2021-06 by ×0.7 (empty stadiums distorted home advantage)

### 4.2 Dixon-Coles dependence correction
Apply the ρ adjustment to the four low-score cells (0-0, 1-0, 0-1, 1-1):

```
τ(x, y) = 1 − λμρ        if (x,y) = (0,0)
        = 1 + λρ          if (x,y) = (0,1)
        = 1 + μρ          if (x,y) = (1,0)
        = 1 − ρ            if (x,y) = (1,1)
        = 1                otherwise
```

Fit ρ jointly with (or after) the GLM by maximum likelihood on the training set. Expected ρ slightly negative (≈ −0.05 to −0.15). Renormalize the matrix after applying τ.

### 4.3 Outputs per match
For each fixture, given λ_A and λ_B:
- 9×9 score matrix (0–8 goals each side, like the reference image; aggregate the tail into the 8 bucket so the matrix sums to 1)
- Derived markets: P(home win), P(draw), P(away win), Over/Under 2.5, BTTS, top-5 most likely exact scores
- Export: one parquet/CSV of all matrices + a rendering function that produces the heatmap table (matplotlib, green→red gradient like the reference)

---

## 5. Backtest Protocol (Qatar 2022)

### 5.1 Prediction generation
- Predict all 48 group matches **as of 2022-11-19** (single freeze; do NOT update Elo between rounds — that matches a "pre-tournament" forecast and avoids round-3 dead-rubber contamination debates; log this decision)
- All World Cup matches in Qatar are neutral-venue **except none** (Qatar's own matches are home; the dataset's `neutral` flag handles this — verify)

### 5.2 Metrics (three layers)
1. **Exact-score hit rate** — count where actual score = modal predicted score. Report it, but label it a vanity metric (expectation: ~5-7/48 for a good model)
2. **Probabilistic scores (primary):**
   - **RPS** (Ranked Probability Score) on 1X2 per match, averaged
   - **Log loss** on the exact-score cell of the actual result (use the 9×9 matrix incl. tail bucket)
   - **Brier score** on 1X2 as secondary
3. **Calibration:** bucket all 1X2 outcome probabilities into deciles, plot predicted vs. realized frequency. 48 matches × 3 outcomes = 144 data points — coarse but indicative

### 5.3 Baselines (all four must be implemented)
| Baseline | Spec |
|---|---|
| B0 — Naive | every match λ = 1.35 / 1.35 |
| B1 — Elo-only | 1X2 directly from Elo expectancy (draw via standard Elo-draw approximation or logistic fit on training data); no score matrix |
| B2 — Market | de-vigged closing 1X2 odds for the 48 matches (source: manually compiled CSV from OddsPortal archive — `data/external/qatar2022_closing_odds.csv`; if compilation fails, mark N/A and proceed) |
| B3 — FiveThirtyEight | their archived 2022 WC match forecasts (publicly archived on GitHub `fivethirtyeight/data`, `soccer-spi`) — if retrievable |

**Success criteria:**
- Must beat B0 decisively and B1 on RPS
- Target: RPS within ~0.01–0.015 of B2 (market). Beating the market is not expected
- Caveat in the report: Qatar 2022 was upset-heavy; 48 matches is a smoke test, not a verdict

### 5.4 Evaluation report
Auto-generated markdown report (`reports/qatar2022_backtest.md`):
- Aggregate metrics table (model vs. all baselines)
- Calibration plot
- Per-match table: fixture, top-3 predicted scores, 1X2 probs, actual score, per-match log loss
- The 5 worst-predicted matches with brief commentary hooks (the Saudi–Argentina row will be fun)
- Rounds 1-2 vs. round 3 metric split (dead-rubber effect)

---

## 6. Repo Structure

```
wc-score-model/
├── README.md                  # project story, headline results, how to run
├── PRD.md                     # this document
├── pyproject.toml             # deps: pandas, numpy, scipy, statsmodels, matplotlib, pytest
├── data/
│   ├── raw/                   # Kaggle snapshot + README with snapshot date
│   ├── processed/             # elo_history.parquet, training table
│   ├── test/                  # qatar2022_group_stage.csv (fixtures + actuals)
│   └── external/              # closing odds, 538 forecasts (optional)
├── src/wcmodel/
│   ├── data.py                # load, clean, build team-match rows
│   ├── elo.py                 # Elo engine (as-of-date ratings)
│   ├── model.py               # Poisson GLM + Dixon-Coles ρ
│   ├── matrix.py              # score matrix + derived markets + heatmap render
│   ├── backtest.py            # freeze logic, prediction generation, metrics (RPS, log loss, Brier, calibration)
│   └── baselines.py           # B0–B3
├── scripts/
│   ├── 01_build_data.py
│   ├── 02_fit_model.py
│   ├── 03_run_backtest.py
│   └── run_all.sh             # one command, end to end
├── notebooks/
│   └── eda.ipynb              # feature exploration, ξ tuning plots
├── reports/                   # generated backtest report + figures
└── tests/
    ├── test_elo.py            # known-result sanity cases
    ├── test_leakage.py        # asserts no post-freeze data in training
    ├── test_matrix.py         # matrix sums to 1, DC correction correct
    └── test_metrics.py        # RPS/log-loss on hand-computed examples
```

---

## 7. Implementation Plan (milestones)

| # | Milestone | Definition of done |
|---|---|---|
| M1 | Data pipeline | Kaggle snapshot loaded, cleaned team-match table built, country-name normalization handled (e.g., "Korea Republic" vs "South Korea") |
| M2 | Elo engine | elo_history.parquet generated; spot-check ~5 teams' Nov-2022 ratings against eloratings.net archive (tolerance ±25 pts) |
| M3 | Model fit | GLM + ξ tuning + DC ρ fitted; coefficients logged and sane (elo_diff > 0, home > 0, ρ < 0) |
| M4 | Matrix + render | Score matrix function tested; heatmap visually matches reference style |
| M5 | Backtest | All 48 predictions generated pre-freeze; metrics vs. B0/B1 computed; B2/B3 if data obtained |
| M6 | Report + README | Auto-report generated; README with headline numbers, one matrix image, run instructions |

Suggested order of Claude Code sessions: M1+M2 together, M3, M4, M5+M6.

---

## 8. Acceptance Criteria (v1 ships when…)

1. `./scripts/run_all.sh` goes from raw CSV → final report with no manual steps
2. `pytest` green, including the leakage test
3. Model beats B0 and B1 on RPS over the 48 matches
4. Elo spot-checks within tolerance
5. Calibration plot shows no gross miscalibration (no decile off by >20pp)
6. README presentable enough to link from an X thread

---

## 9. Risks & Decisions Log

| Risk / decision | Resolution |
|---|---|
| Country naming mismatches across years | Normalization map in `data.py`, unit-tested |
| Elo divergence from eloratings.net | Accept ±25 pts; ours is reproducible, theirs is not |
| Elo deviation concentrated in France | France runs −25 to −45 on pairwise diffs vs one external reference (eloratings.net); persisted across the 1993→1960 burn-in extension; accepted as a modeling difference, not a bug. Flagged so France backtest predictions aren't mis-debugged later. |
| Closing-odds data unobtainable | B2 marked N/A; B0/B1 sufficient for v1 acceptance |
| Single-tournament test variance | Stated caveat; optional stretch: also backtest WC 2018 group stage with freeze at 2018-06-13 (cheap once pipeline exists — recommended if time allows) |
| Tail goals (>8) | Aggregated into the 8-bucket; matrix always sums to 1 |

---

## 10. v2 Hooks (do not build, just don't preclude)

- Per-round Elo updates ("live tournament mode") for 2026
- xG-based λ refinement where FBref coverage exists
- Polymarket odds ingestion for edge detection
- Knockout-stage extension (draw → ET/pens layer)
