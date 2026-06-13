# World Cup Exact-Score Prediction Model

A reproducible **Dixon-Coles Poisson** model that predicts the full exact-score
probability matrix for international football matches — the classic Poisson
score grid (expected goals per side → score-probability matrix → derived 1X2 /
Over-Under / BTTS markets).

**Phase 1 (this repo):** train on data frozen at **2022-11-19** and backtest
against the **Qatar 2022 group stage** (48 matches), with honest baselines.
**Core principle: zero data leakage** — enforced in code, not by convention.

See [`PRD.md`](PRD.md) for the full specification.

## Headline results — Qatar 2022 group stage (48 matches)

Predictions frozen at 2022-11-19, scored against the actual results. Lower is
better. Full auto-generated report: [`reports/qatar2022_backtest.md`](reports/qatar2022_backtest.md).

| Source | RPS ↓ | Log loss ↓ | Brier ↓ |
|---|---|---|---|
| **Model (Dixon-Coles)** | **0.2389** | **3.019** | **0.640** |
| B0 Naive (1.35/1.35) | 0.2398 | 3.071 | 0.647 |
| B1 Elo-only (MNLogit) | 0.2454 | — | 0.653 |
| B2 Market / B3 538 | N/A | N/A | N/A |

### Second tournament (stretch): Russia 2018, frozen at 2018-06-13

Re-running the identical pipeline on a *less upset-heavy* tournament
(`./scripts/run_all.sh russia2018`, report
[`reports/russia2018_backtest.md`](reports/russia2018_backtest.md)):

| Tournament | Model RPS | B0 Naive | B1 Elo | Margin over naive | Hits |
|---|---|---|---|---|---|
| **Russia 2018** | **0.2039** | 0.2425 | 0.2063 | **−0.0386 (decisive)** | 7/48 |
| Qatar 2022 | 0.2389 | 0.2398 | 0.2454 | −0.0009 (thin) | 6/48 |

The thin 2022 margin was the *tournament*, not the model: on 2018 the model
beats naive decisively and calibration is clean (16pp supported-bin max, within
threshold). 2018 is a genuine out-of-sample check — established **before** any
post-2022 model change.

The model **beats both baselines on RPS** (the primary metric) and on Brier and
log loss — passing v1 acceptance. Honest caveats:

- The margin over the naive baseline is **thin (0.0009 RPS)**. Qatar 2022 was
  famously upset-heavy (Saudi over Argentina, Cameroon over Brazil, Japan over
  Germany *and* Spain), and **48 matches is a smoke test, not a verdict** — the
  PRD says as much. B1's confident Elo predictions were punished hardest, so it
  trails even the naive baseline here.
- **Round 3 was far harder** (RPS 0.303) than rounds 1–2 (0.207) — the
  dead-rubber / late-upset effect.
- The model **under-predicts goal totals** (predicted mean total ~0.2–0.4 below
  actual on both tournaments): the worst misses are blowouts (England 6-2 Iran,
  Spain 7-0 Costa Rica). We tried to fix this (see below) — it doesn't generalize.
- Exact-score hit rate **6/48** (in the PRD's expected 5–7 band; a vanity metric).
- Calibration: on well-supported deciles the largest gap is 22.6pp (n=12, ~1.6
  binomial SEs — within noise); the 84pp headline gap is a 2-point bin holding
  exactly the two marquee upsets.

## Status

| Milestone | Description | State |
|---|---|---|
| M1 | Data pipeline (clean, normalize, leakage freeze, team-match rows) | ✅ done |
| M2 | Elo engine (as-of-date ratings) | ✅ done |
| M3 | Poisson GLM + ξ time-decay tuning + Dixon-Coles ρ | ✅ done |
| M4 | Score matrix + heatmap render | ✅ done |
| M5 | Backtest (RPS / log-loss / Brier / calibration) + baselines B0–B3 | ✅ done |
| M6 | Auto report + README headline numbers | ✅ done |

**v1 complete.** `./scripts/run_all.sh` goes raw CSV → report with no manual steps; `pytest` is green (72 tests).

## Quickstart

```bash
pip install -e .            # or: pip install -e ".[dev]"
python scripts/01_build_data.py     # M1+M2: build data, test set, Elo history
pytest -q                           # includes the leakage guard
```

Outputs land in `data/processed/` (`elo_history.parquet`, `team_match.parquet`)
and `data/test/qatar2022_group_stage.csv` (the quarantined test set).

## How it works (so far)

### Data (`src/wcmodel/data.py`)
- Loads the committed [martj42](https://github.com/martj42/international_results)
  snapshot (`data/raw/results.csv`, 1872 → present), keeps played matches.
- Normalizes drifting country names (e.g. *Korea Republic → South Korea*).
- Hard freeze at `FREEZE_DATE = 2022-11-19`; `assert_no_leakage` makes training
  on any later match a runtime error.
- Quarantines the 48 Qatar 2022 group matches into `data/test/` — actual scores
  are never read until the evaluation step.
- Reshapes matches into long team-match rows (one match → two rows), with
  `is_home = 1` only on a non-neutral pitch.

### Elo (`src/wcmodel/elo.py`)
Recomputed from results (not scraped) so we get the rating each team held *on
each match date*. Follows eloratings.net conventions: start 1500, K by
competition (WC 60 / continental 50 / qualifiers 40 / other 30 / friendly 20),
goal-difference multiplier, +100 home advantage (0 on neutral ground),
zero-sum updates, 1960 burn-in, 2000+ trusted as features.

Top of the table at the freeze (2022-11-19), as a sanity check — ordering
matches the known pre-tournament consensus:

| Rank | Team | Elo |
|---|---|---|
| 1 | Brazil | 2234 |
| 2 | Argentina | 2199 |
| 3 | Netherlands | 2115 |
| 4 | Spain | 2110 |
| 5 | Italy | 2070 |

> Our absolute levels run above eloratings.net (≈40–65 pts) because we seed all
> teams flat at 1500 and burn in from 1960; the *ordering* and *spread* are what
> the model consumes, and those align. Per the PRD risk log, we accept this:
> ours is reproducible, theirs is not.

> **Neutral-venue note:** all three of host **Qatar's** group matches are
> non-neutral (`neutral=False`), not just the opener — Qatar is the home side in
> each. Every other group match is played on neutral ground. The dataset's
> `neutral` flag captures this and the model honors it (home advantage applies
> only to Qatar in this tournament).

### Model (`src/wcmodel/model.py`)
A weighted Poisson GLM (log link), `goals ~ intercept + elo_diff + is_home`,
with multiplicative sample weights: exponential time decay `exp(-ξ·days)`,
competition importance (WC/continental 1.0 / qualifier 0.9 / other 0.7 /
friendly 0.5), and a COVID empty-stadium down-weight (×0.7, 2020-03→2021-06).
Then a Dixon-Coles ρ correction fit by MLE on the low-score cells.

`ξ` is tuned by maximizing log-likelihood on a 1-year out-of-sample slice
(full curve → `reports/xi_tuning.csv` + `reports/figures/xi_tuning.png`). The
optional `elo_sum` feature is kept only if it improves the held-out score.

Fitted values at the freeze:

| | value | note |
|---|---|---|
| ξ | 0.0015 /day | half-life ≈ 462 days (~1.3 yr) |
| intercept | +0.048 | even neutral match ≈ 1.05 goals/side |
| elo_diff | +0.768 | stronger team scores more ✓ |
| is_home | +0.254 | ≈ +29% home goal rate ✓ |
| ρ (Dixon-Coles) | −0.048 | slight low-score dependence ✓ |
| elo_sum | dropped | no out-of-sample gain |

A sign gate (`elo_diff > 0`, `is_home > 0`, `ρ < 0`) is asserted in code before
the model is accepted. An **eyeball gate** then prints predicted λs for four
known fixtures (Argentina–Saudi Arabia, Spain–Costa Rica, Brazil–Serbia,
England–Iran) so a flattened slope would be caught before the matrix machinery:

| Fixture (neutral) | λ home | λ away | ratio |
|---|---|---|---|
| Argentina – Saudi Arabia | 2.47 | 0.45 | 5.5× |
| Spain – Costa Rica | 1.68 | 0.66 | 2.6× |
| Brazil – Serbia | 1.76 | 0.63 | 2.8× |
| England – Iran | 1.16 | 0.95 | 1.2× |

The `elo_diff` slope is robust: refitting with friendlies fully excluded moves
it by <0.01 (0.768 → 0.773), so friendlies are not flattening it. A 500-pt Elo
gap maps to a ~6.8× goal ratio (both λs shift), in line with the market shape.

### Score matrix (`src/wcmodel/matrix.py`)
`score_matrix(λ, μ, ρ)` builds the 9×9 exact-score grid in a fixed order:
**(1)** independent Poisson outer product on a wide grid → **(2)** Dixon-Coles τ
on the four low cells → **(3)** fold the 9+ tail into the 8-bucket →
**(4)** renormalize last. The grid sums to 1 to machine precision (tested at
1e-9). `derived_markets` gives 1X2 / O-U 2.5 / BTTS / top-5 scores;
`render_matrix` draws the green→red heatmap.

![sample score matrices](reports/figures/sample_matrices.png)

### Backtest (`src/wcmodel/backtest.py`, `baselines.py`)
Predicts all 48 group matches from the frozen snapshot (Elo *not* updated
between rounds), scores RPS / exact-score log loss / Brier / calibration, and
auto-writes the markdown report with a per-match table, the 5 worst misses, and
the round split. Baselines B0 (naive) and B1 (Elo-only multinomial logit) are
implemented; B2 (de-vigged closing odds) and B3 (538) are wired with documented
CSV schemas but N/A here — odds weren't compiled and 538's data is offline.

### v1.1 experiment: the goal-level fix that *didn't* generalize

The goal under-prediction looked like an easy win — give WC finals (or neutral
matches) their own intercept. Tested on 2022 alone, a neutral-venue effect nails
the total (predicted 2.28 → 2.54 vs actual 2.50). But validated against **2018
out-of-sample first** (`scripts/experiment_goal_level.py`, writeup in
[`reports/goal_level_experiment.md`](reports/goal_level_experiment.md)), both
candidate fixes fail a pre-registered rule (improve RPS on *both* tournaments):

| Fix | coef Qatar / 2018 | RPS Qatar | RPS 2018 | verdict |
|---|---|---|---|---|
| `is_wc` | +0.17 / +0.03 | worse | ~flat | reject |
| `is_neutral` | +0.24 / +0.40 | worse | better | reject |

Each fix is tuned to whichever tournament it sees, the coefficient is unstable
across freezes, it overshoots the other tournament, and it tends to *worsen* the
primary metric. This is the textbook overfit the **(b)-before-(a) ordering was
designed to catch** — deferred to v2 honestly rather than baked in. The shipped
model is unchanged.

## Forward prediction (current Elo)

The backtest stays frozen at 2022-11-19, but you can predict any fixture from
**current** ratings:

```bash
# Quick single-fixture prediction from current Elo (no build step needed):
python scripts/predict_match.py 'Mexico' 'South Africa' --home Mexico
python scripts/predict_match.py 'Brazil' 'Argentina'           # neutral venue

# Optionally rebuild persisted Elo/team_match up to any date:
python scripts/01_build_data.py --freeze-date 2026-06-10        # -> data/processed/asof_2026-06-10/
```

### 2026 World Cup group stage (update-as-you-go)

The snapshot already carries the full 72-fixture 2026 group stage with correct
host/neutral flags. `predict_fixtures.py` predicts **each team's next unplayed
group match** from current Elo (the openers now, the next matchday after results
land), writing `reports/wc2026_predictions.csv`:

```bash
python scripts/predict_fixtures.py            # each team's next match (24 now)
python scripts/predict_fixtures.py --refresh  # pull latest results, then predict
python scripts/predict_fixtures.py --all      # all remaining group games
python scripts/predict_fixtures.py --plot     # also save per-fixture heatmaps
```

The loop: run → play the matches → `--refresh` re-pulls results so Elo updates →
re-run for the next matchday. Model coefficients stay frozen at the
backtest-validated 2022-11-19 fit; only the ratings move. Knockouts are out of
scope (no ET/penalties layer yet).

**Recording results before the upstream feed updates.** Drop known scores into
`data/external/wc2026_results.csv` (`date, home_team, away_team, home_score,
away_score`); they're folded onto the snapshot so Elo updates and the fixtures
drop out of "upcoming" immediately (redundant once `--refresh` pulls the
official result).

**Market as a comparison / edge layer (not a model input).** If
`data/external/wc2026_odds.csv` holds bookmaker odds (`home_team, away_team,
odds_home, odds_draw, odds_away` — **fractional, decimal, or US moneyline** like
`-160`/`+260`), `predict_fixtures.py`
de-vigs them and shows market H/D/A beside ours, flags fixtures where they
disagree by ≥ `--edge` (default 0.10), and accumulates a forward log
(`data/external/wc2026_forward_log.csv`) of pre-match forecast + market +
backfilled result. Once matches are played it scores **model vs market RPS** —
the B2 baseline, finally measured forward. The model and the frozen backtest are
never touched; the odds are deliberately *beside* the model, so disagreements
stay visible (they turn out to track the model's known weak spots — host
calibration and favourite-compression). The decision rationale is in
[`reports/odds_integration_decision.md`](reports/odds_integration_decision.md).

`predict_match.py` computes Elo over every played match (current), applies the
fitted Dixon-Coles model, and prints the score matrix, 1X2 / O-U / BTTS, and
top-5 scores. The `--freeze-date` flag routes non-default builds to
`data/processed/asof_<date>/`, so the **frozen backtest artifacts are never
touched** — and `03_run_backtest.py` asserts its model was frozen at the
tournament cutoff, failing loudly if it ever isn't.

## Live page & daily automation

A simple static page (`docs/index.html`, built by `scripts/build_site.py`) shows
the **next 4 kickoffs** with our 1X2 (probability + fair odds), top-3 scorelines,
the market price, and the model's EV — plus a running model-vs-market RPS strip.

`.github/workflows/daily.yml` runs **06:00 UTC daily** (= 09:00 Israel during the
summer tournament) and on demand: fetch odds → refresh results & Elo → rebuild
the page and report → commit back. To enable it:

1. Make `main` the **default branch** (scheduled Actions only fire from default).
2. **Settings → Pages → Deploy from branch → `main` / `docs`** (the page is public).
3. Add repo secret **`ODDS_API_KEY`** from [the-odds-api.com](https://the-odds-api.com)
   (free tier; `scripts/fetch_odds.py` pulls `soccer_fifa_world_cup` h2h odds and
   writes the median price per fixture). Everything is **fail-soft**: no key or a
   bad response just keeps the existing odds CSV, so the page never breaks.

```bash
python scripts/build_site.py          # rebuild docs/index.html
ODDS_API_KEY=xxxx python scripts/fetch_odds.py   # refresh market odds
```

## Repo layout

```
src/wcmodel/   data.py · elo.py · model.py · matrix.py · backtest.py · baselines.py
scripts/       01_build_data.py · 02_fit_model.py · 03_run_backtest.py · run_all.sh
               predict_match.py · predict_fixtures.py · experiment_goal_level.py
data/          raw/ · processed/ · test/ · external/
tests/         test_elo.py · test_leakage.py · test_model.py · test_matrix.py · test_metrics.py
```
