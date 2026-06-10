# v1.1 Experiment — Goal-Level (Intercept) Fix

The v1 model under-predicts goal totals on WC finals. We test two intercept-level fixes and ask whether either **generalizes** across both frozen tournaments. Russia 2018 is the independent out-of-sample check, established with the v1 pipeline *before* this experiment.

**Adoption rule (set in advance):** adopt only if RPS (primary) improves out-of-sample on *both* tournaments. Lower RPS / log loss / Brier is better.

## Qatar 2022  (actual mean total 2.50)

| Variant | added coef | RPS | Log loss | Brier | pred. total |
|---|---|---|---|---|---|
| v1 (base) | — | 0.2389 | 3.0188 | 0.6401 | 2.28 |
| + is_wc | +0.166 (1.18×) | 0.2408 | 3.0156 | 0.6411 | 2.69 |
| + is_neutral | +0.235 (1.27×) | 0.2424 | 3.0173 | 0.6460 | 2.54 |

## Russia 2018  (actual mean total 2.54)

| Variant | added coef | RPS | Log loss | Brier | pred. total |
|---|---|---|---|---|---|
| v1 (base) | — | 0.2029 | 2.8131 | 0.5634 | 2.37 |
| + is_wc | +0.025 (1.03×) | 0.2026 | 2.8100 | 0.5621 | 2.43 |
| + is_neutral | +0.401 (1.49×) | 0.2016 | 2.8544 | 0.5579 | 2.87 |

## Verdict

- **+ is_wc**: Qatar 2022 ΔRPS +0.0019, Russia 2018 ΔRPS -0.0003 → REJECT (does not improve RPS on both).
  Coefficient is unstable across freezes (Qatar 2022 +0.166, Russia 2018 +0.025), confirming it fits the in-sample tournament rather than a structural effect.

- **+ is_neutral**: Qatar 2022 ΔRPS +0.0035, Russia 2018 ΔRPS -0.0012 → REJECT (does not improve RPS on both).
  Coefficient is unstable across freezes (Qatar 2022 +0.235, Russia 2018 +0.401), confirming it fits the in-sample tournament rather than a structural effect.

**Conclusion:** neither fix is adopted. The goal-level bias is real and consistent in direction, but both candidate corrections are tuned to whichever tournament they see, overshoot the other, and tend to worsen RPS — the textbook failure the (b)-before-(a) ordering was meant to catch. Deferred to v2 (richer attack/defence + competition-aware dispersion, validated on more than two tournaments).
