#!/usr/bin/env python3
"""Diagnostic: does the Elo-gap → goals curve bend enough at large mismatches?

Settles which of three failure modes explains blowout under-prediction:

  A  Curve too flat  — log λ should be convex at large elo_diff; the Elo gap
                       isn't scaling goal output hard enough for big mismatches.
  B  Elo compression — minnow teams with thin, regional schedules never get
                       "marked down" by blowout defeats, so their Elo stays
                       too high and the gap is understated as a model input.
  C  Tail too thin   — the mean λ is fine but Poisson (Var = Mean by law)
                       starves the 5-0 / 7-1 region; a fatter-tailed distribution
                       is needed, not a higher mean.

Method: bin all 20-year training matches by the team's Elo advantage, compare
mean actual goals scored to the model's predicted λ per bin, and measure
over-dispersion (Var/Mean > 1 = Fork C signal).

Outputs (all under reports/):
    reports/figures/gap_curve.png       two-panel diagnostic plot
    reports/gap_curve_bins.csv          per-bin stats table
    reports/gap_curve_diagnostic.md     auto-generated verdict

Strictly read-only with respect to the model and all forward / 2026 data.
Run: python scripts/diag_gap_curve.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import poisson

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel.data import FEATURE_START, FREEZE_DATE, PROCESSED, ROOT  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

# ---------------------------------------------------------------------------
# Known 2026 WC teams (48) for the Fork-B minnow table
# ---------------------------------------------------------------------------
WC2026_TEAMS = [
    "Argentina", "Algeria", "Australia", "Austria", "Belgium",
    "Bolivia", "Bosnia and Herzegovina", "Brazil", "Canada", "Cape Verde",
    "Colombia", "Croatia", "Czech Republic", "Curaçao", "DR Congo",
    "Ecuador", "Egypt", "England", "France", "Germany",
    "Ghana", "Haiti", "Iran", "Iraq", "Ivory Coast",
    "Japan", "Jordan", "Mexico", "Morocco", "Netherlands",
    "New Zealand", "Norway", "Panama", "Paraguay", "Portugal",
    "Qatar", "Saudi Arabia", "Scotland", "Senegal", "South Africa",
    "South Korea", "Spain", "Sweden", "Switzerland", "Tunisia",
    "Turkey", "United States", "Uruguay", "Uzbekistan",
]

TOP30_N = 30
MIN_BIN_N = 30   # hide bins with fewer rows from the plot
BIN_WIDTH = 0.25

# Approximate elo_diff (team/400) for the two headline 2026 fixtures,
# back-computed from the published λ using frozen coefficients.
HIGHLIGHT_GAPS = {
    "Ger–Curaçao": 0.965,
    "ESP–CapeVerde": 1.436,
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_training(model: FittedModel) -> pd.DataFrame:
    df = pd.read_parquet(PROCESSED / "team_match.parquet")
    assert df["date"].max() <= FREEZE_DATE, "leakage in training table"
    df = df[df["date"] >= FEATURE_START].copy()
    df["elo_diff"] = (df["team_elo_pre"] - df["opp_elo_pre"]) / 400.0
    df["model_lam"] = model.predict_lambdas(df)
    return df


# ---------------------------------------------------------------------------
# Fork A + C: bin analysis
# ---------------------------------------------------------------------------

def compute_bins(df: pd.DataFrame) -> pd.DataFrame:
    edges = np.arange(-3.0 - BIN_WIDTH / 2, 3.0 + BIN_WIDTH, BIN_WIDTH)
    df = df.copy()
    df["bin"] = pd.cut(df["elo_diff"], bins=edges)

    def _stats(g: pd.DataFrame) -> pd.Series:
        n = len(g)
        acts = g["goals_for"].to_numpy(dtype=float)
        lams = g["model_lam"].to_numpy(dtype=float)
        mean_act = acts.mean()
        mean_lam = lams.mean()
        var = acts.var(ddof=0)
        # Per-row Poisson SF, then averaged (Jensen-correct vs using mean λ)
        p5_pois = float(poisson.sf(4, lams).mean())
        p5_act = float((acts >= 5).mean())
        return pd.Series({
            "n": n,
            "mean_actual": round(mean_act, 3),
            "mean_lambda": round(mean_lam, 3),
            "residual": round(mean_act - mean_lam, 3),
            "var_over_mean": round(var / mean_act, 3) if mean_act > 0 else np.nan,
            "p_ge5_actual": round(p5_act, 4),
            "p_ge5_poisson": round(p5_pois, 4),
        })

    result = df.groupby("bin", observed=True).apply(_stats).reset_index()
    # Use list comprehension — avoids Categorical dtype propagation from .apply()
    result["mid"] = [float(round(iv.mid, 4)) for iv in result["bin"]]
    return result


# ---------------------------------------------------------------------------
# Fork B: minnow schedule-isolation analysis
# ---------------------------------------------------------------------------

def compute_minnow_table(df: pd.DataFrame) -> pd.DataFrame:
    # Latest Elo at or before freeze
    eh = pd.read_parquet(PROCESSED / "elo_history.parquet")
    latest_elo = (
        eh[eh["date"] <= FREEZE_DATE]
        .sort_values("date")
        .groupby("team")["rating_post_match"]
        .last()
        .reset_index()
        .rename(columns={"rating_post_match": "elo_at_freeze"})
    )

    top30 = set(
        latest_elo.nlargest(TOP30_N, "elo_at_freeze")["team"]
    )

    # Training matches per team (total) and vs top-30 opponents
    total_matches = df.groupby("team").size().rename("n_train_matches")
    vs_top30 = (
        df[df["opponent"].isin(top30)]
        .groupby("team").size()
        .rename("n_vs_top30")
    )

    wc = latest_elo[latest_elo["team"].isin(WC2026_TEAMS)].copy()
    wc = wc.merge(total_matches, on="team", how="left")
    wc = wc.merge(vs_top30, on="team", how="left")
    wc["n_vs_top30"] = wc["n_vs_top30"].fillna(0).astype(int)
    wc["n_train_matches"] = wc["n_train_matches"].fillna(0).astype(int)
    wc["pct_vs_top30"] = np.where(
        wc["n_train_matches"] > 0,
        (wc["n_vs_top30"] / wc["n_train_matches"] * 100).round(1),
        np.nan,
    )
    wc["elo_rank_wc"] = wc["elo_at_freeze"].rank(ascending=False).astype(int)
    return wc.sort_values("elo_at_freeze")


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

def make_plot(bins: pd.DataFrame, out_path: Path) -> None:
    b = bins[bins["n"] >= MIN_BIN_N].copy()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True,
                                    gridspec_kw={"hspace": 0.08})

    # --- Panel 1: actual goals vs model λ ---
    sizes = np.clip(b["n"] / 8, 20, 400)
    sc = ax1.scatter(b["mid"], b["mean_actual"], s=sizes, color="#1976D2",
                     alpha=0.85, zorder=4, label="actual mean goals (size ∝ n)")
    ax1.plot(b["mid"], b["mean_lambda"], color="#E53935", lw=2.0, zorder=3,
             label="model λ (predicted)")

    # shaded region where dots are clearly above the line
    ax1.fill_between(b["mid"],
                     b["mean_lambda"],
                     np.maximum(b["mean_actual"], b["mean_lambda"]),
                     alpha=0.12, color="#43A047", label="actual > λ (Fork A signal)")

    for label, gap in HIGHLIGHT_GAPS.items():
        ax1.axvline(gap, color="#9E9E9E", ls="--", lw=1.2, zorder=2)
        ax1.text(gap + 0.04, b["mean_actual"].max() * 0.92,
                 label, fontsize=8, color="#616161", va="top")

    ax1.axhline(0, color="#BDBDBD", lw=0.6)
    ax1.set_ylabel("Goals scored per team-match", fontsize=11)
    ax1.set_title(
        "Elo advantage → goal output: actual vs. model (training data 2000–2022)",
        fontsize=12, fontweight="bold",
    )
    ax1.legend(fontsize=9, loc="upper left")
    ax1.grid(True, alpha=0.25)

    # --- Panel 2: residual + Var/Mean ---
    bar_colors = np.where(b["residual"] > 0, "#43A047", "#EF5350")
    ax2.bar(b["mid"], b["residual"], width=BIN_WIDTH * 0.85,
            color=bar_colors, alpha=0.75, zorder=3, label="residual actual − λ")
    ax2.axhline(0, color="#616161", lw=1.0)

    ax2b = ax2.twinx()
    ax2b.plot(b["mid"], b["var_over_mean"], color="#FF6F00", lw=2.0,
              marker="o", markersize=4, zorder=4, label="Var/Mean (Poisson = 1.0)")
    ax2b.axhline(1.0, color="#FF6F00", lw=1.0, ls="--", alpha=0.6)

    for label, gap in HIGHLIGHT_GAPS.items():
        ax2.axvline(gap, color="#9E9E9E", ls="--", lw=1.2, zorder=2)

    ax2.set_xlabel("Elo advantage  (team − opponent) / 400", fontsize=11)
    ax2.set_ylabel("Residual (goals)", fontsize=10)
    ax2b.set_ylabel("Var / Mean  [Poisson = 1.0]", fontsize=10, color="#FF6F00")
    ax2b.tick_params(axis="y", colors="#FF6F00")

    lines_a, labs_a = ax2.get_legend_handles_labels()
    lines_b, labs_b = ax2b.get_legend_handles_labels()
    ax2.legend(lines_a + lines_b, labs_a + labs_b, fontsize=9, loc="upper left")
    ax2.grid(True, alpha=0.25)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  plot  →  {out_path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def write_report(bins: pd.DataFrame, minnows: pd.DataFrame, out_path: Path) -> None:
    b = bins[bins["n"] >= MIN_BIN_N]

    # Compute diagnostic signals
    big_gap = b[b["mid"] >= 1.0]

    fork_a_residual = big_gap["residual"].mean() if len(big_gap) else np.nan
    fork_a_verdict = (
        "**CONFIRMED** — actual goals systematically above model curve at large gaps"
        if fork_a_residual > 0.20 else
        "**WEAK / NOT CONFIRMED** — residual at large gaps not substantially positive"
    )

    fork_c_varMean = b["var_over_mean"].median()
    fork_c_big = big_gap["var_over_mean"].mean() if len(big_gap) else np.nan
    fork_c_verdict = (
        "**CONFIRMED** — Var/Mean consistently > 1.2 across bins (over-dispersed)"
        if fork_c_varMean > 1.15 else
        "**WEAK / NOT CONFIRMED** — Var/Mean near 1.0; Poisson dispersion roughly ok"
    )

    # Fork B: minnows with < 5% vs top-30
    isolated = minnows[minnows["pct_vs_top30"] < 5].sort_values("pct_vs_top30")
    fork_b_verdict = (
        f"**LIKELY for {len(isolated)} teams** — very low % of training matches vs top-30"
        if len(isolated) >= 2 else
        "**WEAK** — most WC2026 minnows have reasonable top-30 exposure"
    )

    # Per-bin markdown table (only key columns, high-gap bins)
    table_cols = ["mid", "n", "mean_actual", "mean_lambda", "residual",
                  "var_over_mean", "p_ge5_actual", "p_ge5_poisson"]
    notable = b[b["mid"].abs() >= 0.75][table_cols].copy()

    # Minnow table (bottom 15 by Elo)
    minnow_display = minnows.nsmallest(15, "elo_at_freeze")[
        ["team", "elo_at_freeze", "elo_rank_wc", "n_train_matches",
         "n_vs_top30", "pct_vs_top30"]
    ]

    lines = [
        "# Gap-curve diagnostic — Fork A / B / C verdict",
        "",
        f"Generated from: `team_match.parquet` (training window "
        f"{FEATURE_START.date()} → {FREEZE_DATE.date()}, frozen coefficients).",
        "",
        "![gap curve](figures/gap_curve.png)",
        "",
        "## Verdicts",
        "",
        f"| Fork | Hypothesis | Signal | Verdict |",
        f"|---|---|---|---|",
        f"| **A** | Curve too flat at large Elo gaps | mean residual (actual−λ) at elo_diff ≥ 1.0: "
        f"`{fork_a_residual:+.3f}` | {fork_a_verdict} |",
        f"| **C** | Poisson tail too thin | median Var/Mean across bins: `{fork_c_varMean:.3f}`; "
        f"at large gaps: `{fork_c_big:.3f}` | {fork_c_verdict} |",
        f"| **B** | Minnow Elo compressed | {len(isolated)} WC2026 teams with <5% top-30 matches | "
        f"{fork_b_verdict} |",
        "",
        "## Reading the plot",
        "",
        "- **Top panel:** dots = actual mean goals per bin (size ∝ n matches); "
        "red line = model λ. Green shading = region where actual > λ (Fork A signal).",
        "- **Bottom panel:** green/red bars = residual (actual − λ). "
        "Orange line = Var/Mean ratio; dashed line at 1.0 = Poisson baseline (Fork C signal).",
        "- Vertical dashed lines mark the Germany–Curaçao and Spain–Cape Verde Elo gaps.",
        "",
        "## Per-bin stats (|elo_diff| ≥ 0.75)",
        "",
        notable.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Fork B — minnow schedule isolation (bottom 15 WC2026 teams by Elo at freeze)",
        "",
        "> `pct_vs_top30` = % of 2000–2022 training matches played against top-30 opponents.",
        "> Teams below ~5% have Elo ratings that were never stress-tested against elites —",
        "> their gap with tournament-calibre sides is likely understated.",
        "",
        minnow_display.to_markdown(index=False, floatfmt=".1f"),
        "",
        "## Implications for the model",
        "",
        "- **If Fork A confirmed:** add `elo_diff²` (or a spline) to the GLM. "
        "Refit and run through the two-tournament gate (Qatar 2022 + Russia 2018) "
        "before touching any live predictions.",
        "- **If Fork B confirmed:** apply per-team Elo shrinkage toward confederation "
        "priors for teams with <10% top-30 exposure. Input fix — does not require "
        "re-fitting the GLM.",
        "- **If Fork C confirmed:** swap Poisson → Negative-Binomial (or Poisson-Gamma). "
        "One extra dispersion parameter; refit by MLE, run two-tournament gate.",
        "- **Multiple forks confirmed:** fix in order C → B → A (least model risk first).",
        "",
        "Reminder: no model change goes live mid-tournament. All experiments must "
        "improve RPS on *both* backtests (pre-registration rule from `reports/goal_level_experiment.md`).",
    ]

    out_path.write_text("\n".join(lines))
    print(f"  report →  {out_path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Loading model and training data …")
    model = FittedModel.load(PROCESSED / "model.json")
    df = load_training(model)
    print(f"  {len(df):,} team-match rows  ({FEATURE_START.date()} → {FREEZE_DATE.date()})")

    print("Computing bin stats …")
    bins = compute_bins(df)

    print("Computing minnow table …")
    minnows = compute_minnow_table(df)

    out_fig = ROOT / "reports" / "figures" / "gap_curve.png"
    out_csv = ROOT / "reports" / "gap_curve_bins.csv"
    out_md  = ROOT / "reports" / "gap_curve_diagnostic.md"

    print("Generating outputs …")
    make_plot(bins, out_fig)
    bins.to_csv(out_csv, index=False)
    print(f"  csv   →  {out_csv.relative_to(ROOT)}")
    write_report(bins, minnows, out_md)

    # Summary printout
    b = bins[bins["n"] >= MIN_BIN_N]
    big_gap = b[b["mid"] >= 1.0]
    print(f"\n── Quick verdict ──────────────────────────────────────")
    print(f"  Fork A residual at elo_diff ≥ 1.0 : {big_gap['residual'].mean():+.3f}  "
          f"(>+0.20 = confirmed)")
    print(f"  Fork C median Var/Mean            : {b['var_over_mean'].median():.3f}  "
          f"(>1.15 = confirmed)")
    isolated = minnows[minnows["pct_vs_top30"] < 5]
    print(f"  Fork B isolated minnows (<5% top30): {len(isolated)} WC2026 teams")
    if len(isolated):
        for _, row in isolated.iterrows():
            print(f"    {row['team']:<25} Elo {row['elo_at_freeze']:.0f}  "
                  f"{row['pct_vs_top30']:.1f}% vs top-30")
    print(f"───────────────────────────────────────────────────────")


if __name__ == "__main__":
    main()
