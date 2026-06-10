# Betting Odds: Comparison Layer, Not a Model Input

**Decision:** de-vigged market odds are shown *beside* the model and logged for
forward scoring — they are **not** blended into the model or used as a feature.
The Dixon-Coles model and the frozen backtest stay independent.

## Why not blend the market in

1. **The market is at/near the ceiling.** The PRD already expects we won't beat
   it. Blending (`p = w·model + (1−w)·market`) would mostly make us *report the
   market*, and "we beat baseline X" becomes circular once the market is inside.
2. **We can't validate a blend.** There are no historical closing odds (B2 was
   N/A for 2022 and 2018), so any blend weight or odds-feature is a knob we
   cannot backtest. Bolting an unvalidated component onto a validated model
   trades away the project's main asset — a clean, leakage-free evaluation.
3. **Disagreements are the value.** Kept side-by-side, the market is a live
   diagnostic of where the model is wrong.

## What the disagreements already show (matchday 1)

De-vigging the opening odds and differencing against the model surfaced a
*structured* pattern, not noise:

- **Host calibration is off, team-specifically** — model vs market on the home
  side: Canada **+0.19**, Mexico **+0.11**, but USA **−0.16**. A flat +100 Elo
  home bonus can't capture team-specific host strength the market prices in.
- **Favourite-compression** — the model is *less* confident than the market on
  Brazil (−0.14), Netherlands (−0.11), France (−0.08): the same upset-sensitivity
  seen in the backtests.
- **Agreement on clean favourites** — Spain–Cape Verde (+0.02), Argentina–Algeria
  (+0.01).

These line up with the model's already-documented weak spots, so the comparison
earns its keep as a diagnostic.

## What we built

- `src/wcmodel/odds.py` — parse (fractional/decimal), de-vig, align to fixtures.
- `data/external/wc2026_odds.csv` — bookmaker odds (user-maintained).
- `predict_fixtures.py` — market H/D/A + an edge flag (`|Δ| ≥ --edge`) beside the
  model, plus an edge summary of the biggest disagreements.
- `data/external/wc2026_forward_log.csv` — accumulates {pre-match forecast,
  market, backfilled result}. Predictions are logged **once** (never overwritten),
  results are filled from the snapshot keyed on (home, away, **date**).

## The forward path

Logging now turns the can't-backtest problem into a data-collection opportunity:
once group matches are played, `predict_fixtures.py` scores **model vs market
RPS** over completed fixtures — B2, measured honestly going forward. Only after a
meaningful sample (and with an out-of-sample weight) would an explicit blend be
worth revisiting. Until then: pure model, market in the next column.
