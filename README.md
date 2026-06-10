# World Cup Exact-Score Prediction Model

A reproducible **Dixon-Coles Poisson** model that predicts the full exact-score
probability matrix for international football matches — the classic Poisson
score grid (expected goals per side → score-probability matrix → derived 1X2 /
Over-Under / BTTS markets).

**Phase 1 (this repo):** train on data frozen at **2022-11-19** and backtest
against the **Qatar 2022 group stage** (48 matches), with honest baselines.
**Core principle: zero data leakage** — enforced in code, not by convention.

See [`PRD.md`](PRD.md) for the full specification.

## Status

| Milestone | Description | State |
|---|---|---|
| M1 | Data pipeline (clean, normalize, leakage freeze, team-match rows) | ✅ done |
| M2 | Elo engine (as-of-date ratings) | ✅ done |
| M3 | Poisson GLM + ξ time-decay tuning + Dixon-Coles ρ | ⬜ next |
| M4 | Score matrix + heatmap render | ⬜ |
| M5 | Backtest (RPS / log-loss / Brier / calibration) + baselines B0–B3 | ⬜ |
| M6 | Auto report + README headline numbers | ⬜ |

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
zero-sum updates, 1993 burn-in, 2000+ trusted as features.

Top of the table at the freeze (2022-11-19), as a sanity check — ordering
matches the known pre-tournament consensus:

| Rank | Team | Elo |
|---|---|---|
| 1 | Brazil | 2207 |
| 2 | Argentina | 2171 |
| 3 | Netherlands | 2074 |
| 4 | Spain | 2071 |
| 5 | Italy | 2030 |

> Our absolute levels run ~30–40 pts above eloratings.net because we seed all
> teams flat at 1500 and burn in from 1993; the *ordering* and *spread* are what
> the model consumes, and those align. Per the PRD risk log, we accept this:
> ours is reproducible, theirs is not.

## Repo layout

```
src/wcmodel/   data.py · elo.py  (model.py · matrix.py · backtest.py · baselines.py to come)
scripts/       01_build_data.py  (02_fit_model.py · 03_run_backtest.py to come)
data/          raw/ · processed/ · test/ · external/
tests/         test_elo.py · test_leakage.py  (test_matrix.py · test_metrics.py to come)
```
