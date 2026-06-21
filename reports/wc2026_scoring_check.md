# 2026 World Cup: is it really high-scoring, and what should xG do about it?

*Generated 2026-06-21, on the first 36 completed group-stage matches.*
*Sources: `reports/wc2026_forward_scored.csv`, `data/external/wc2026_forward_log.csv`,
`data/raw/results.csv`. Reproduce with the snippets quoted below.*

## TL;DR

1. **The claim is real but not yet nailed down.** 2026 is running at **3.03
   goals/match** vs a 2002–2022 World Cup average of **2.51** and a recent high
   of **2.69** (2022). Our model's xG expected **2.48/match**, so actual goals
   are **+22% over xG** (109 actual vs 89.2 xG, +19.8 goals). That excess is
   **~2.1σ over the model** and **~2.0σ over the historical rate** on 36 games —
   *suggestive, not decisive*. Treat it the way the repo treats everything: a
   strong signal worth instrumenting, not yet a verdict (cf. "48 matches is a
   smoke test" in the README).
2. **The miss is a *level* miss, not a *slope* miss.** Favourites over-score by
   1.22× and underdogs by 1.24× — almost identical. The Elo slope is fine; the
   whole goal level is low. The 1X2 ratios are roughly right; the *totals and
   exact scores* (our primary objective) are biased low.
3. **There is genuine over-dispersion.** Team-score variance/mean = **1.52**
   (Poisson assumes 1.0), and team-scores ≥4 happened **9** times vs **4.2**
   expected under Poisson. The blowouts (Germany 7-1, Canada 6-0, Sweden 5-1,
   Netherlands 5-1) are a *fat tail the Poisson structurally cannot produce*.

## Verification detail

| Metric | Value |
|---|---|
| Completed matches | 36 |
| Actual goals | 109 (**3.03**/match) |
| Model xG (v2, already includes the 1.10 uplift) | 89.2 (2.48/match) |
| Actual / xG | **1.222** (bias +19.8) |
| P(≥109 goals \| mean 89.2), Poisson | 0.023 (z ≈ 2.10) |
| z vs historical 2.51/match | 1.96 |
| z vs 2022's 2.69/match | 1.24 |
| Matches ≥4 goals | 14 / 36 (39%) |

Historical WC goals/match: 2010 **2.27** · 2014 **2.67** · 2018 **2.64** ·
2022 **2.69** · **2026 3.03**. Even the most offensive recent edition sits well
below 2026.

**Where the excess sits (residual decomposition):**

| Split | xG | Actual | ratio |
|---|---|---|---|
| Favourite side (by λ) | 61.7 | 75 | 1.22 |
| Underdog side (by λ) | 27.5 | 34 | 1.24 |
| Listed-home side | 51.9 | 73 | **1.41** |
| Listed-away side | 37.3 | 36 | 0.96 |

The favourite/underdog symmetry says "lift the level, don't steepen the slope."
The listed-home/away tilt is eye-catching (almost all these games are on
*neutral* ground, so the model gives no home bump) — but on 36 matches it is
just as likely a "designated-home" artifact as a real effect. **Flag, don't
act** (see tweak D).

## "It might be the water breaks" — taking the heat hypothesis seriously

2026 is the first World Cup played across **extreme-heat North American summer
afternoon venues** (Dallas, Houston, Monterrey, Kansas City…) with **mandatory
cooling/hydration breaks**. The mechanism people are pointing at is plausible:

- Heat → lower pressing intensity and earlier fatigue → stretched, transitional
  games → more space → more goals.
- Cooling breaks → mid-half tactical resets and recovery → can tilt open games.

**But it is currently unfalsifiable on our backtests.** Both validation
tournaments had *no* heat regime: Russia 2018 was mild, Qatar 2022 was a winter
tournament in air-conditioned stadiums. So a heat/cooling-break feature **cannot
pass the repo's "improve both backtests" rule** — it can only be tested *forward,
on 2026 itself*. That doesn't make it wrong; it makes it a hypothesis we must
instrument rather than assume.

**Good news: the data needed is already half-here.** `data/raw/results.csv`
carries `city` and `country` per match, so each 2026 fixture can be joined to a
**venue + local kickoff temperature** (and a cooling-break flag, e.g. WBGT >
32 °C, which is the FIFA trigger). Then the test is one regression: per-match
goal *residual* (actual − xG) on kickoff temperature. If the +22% concentrates
in the hot afternoon games and the cool/roofed/evening games sit near 1.0, the
water-break story holds and earns a feature. If the excess is flat across
temperature, it's a global-level miss and the heat story is a red herring.

*(I could not run that regression here — kickoff time and temperature aren't in
the dataset yet. Attaching them is step 1 of tweak C below.)*

## Proposed xG tweaks (ranked, and consistent with the repo's discipline)

The repo's culture is explicit: no tweak gets hard-coded off in-tournament data,
and the v1.1 goal-level experiment was *rejected* precisely because it overfit
one tournament. None of the below should touch the frozen backtest; they are
**v3 forward proposals**.

### A. Re-fit the global `goal_scale` — but shrink it, don't chase 1.34
v2 already multiplies both λ by 1.10 and we're *still* +22%. The naive update is
1.10 × 1.22 ≈ **1.34**, but that over-fits 36 high-variance, opener-heavy games
(matchday-1/2 are historically more open; round-3 dead rubbers pull back down).
Recommendation: a **shrunk, live scale** — a Bayesian/EWMA blend of the 1.10
prior and the observed ratio, weighted by sample size — so the scale drifts up
*as evidence accumulates* instead of snapping to a small-sample point estimate.
Symmetric, so it sharpens totals/exact-score (our primary metric) without moving
the 1X2 ratio. **Biggest single lever; lowest risk if shrunk.**

### B. Swap Poisson → Negative Binomial (model the over-dispersion)
var/mean = 1.52 and the ≥4-goal tail (9 vs 4.2 expected) are textbook
over-dispersion. A Poisson-Gamma / Negative-Binomial mixture adds **one
dispersion parameter** and fattens the tail, fixing exactly the blowout
under-prediction the README already lists as the worst misses (England 6-2 Iran,
Spain 7-0 Costa Rica). Crucially this is a **structural** change that **can be
validated on 2018 + 2022** — so it can pass the both-backtests rule and graduate
properly. **Highest-quality tweak; do it the disciplined way.**

### C. Instrument the heat / cooling-break hypothesis (don't bake it in)
1. Join `city`/`country` → venue → local kickoff temperature + a `cooling_break`
   flag per 2026 fixture.
2. Regress per-match goal residual on temperature; split hot vs cool.
3. *Only if* the excess is demonstrably hot-venue-driven, add an `is_hot` /
   temperature λ-multiplier as a **forward-only v3 feature** with a
   pre-registered hot/cool split (it can't use 2018/2022, so it must be honest
   about being 2026-only and re-checked as games accrue).

### D. Watch, don't touch: the listed-home tilt (1.41 vs 0.96 on neutral games)
Possibly a real "designated home team" edge (familiar end, logistics, fan
share), possibly pure noise on 36 matches. Revisit at n ≥ 64 before considering a
neutral-venue nominal-home term.

## Recommended order of operations
1. **B first** (Negative-Binomial) — it's the one tweak that fixes a real,
   measured defect (over-dispersion / blowout tail) *and* can be validated
   out-of-sample on both backtests, so it graduates honestly.
2. **A second** — turn the fixed 1.10 into a shrunk live scale; re-estimate as
   the group stage completes rather than committing to 1.34 now.
3. **C in parallel as data collection** — attach temperatures now so that by the
   end of the group stage we can actually answer the water-break question
   instead of speculating.
4. **D: monitor only.**

> Nothing here changes the frozen 2022-11-19 backtest or the shipped v1/v2
> models. These are proposals to be validated under the repo's existing
> b-before-a / both-backtests rules before anything ships.
