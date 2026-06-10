#!/usr/bin/env python3
"""M3: fit the Poisson GLM (with xi tuning) and the Dixon-Coles rho.

Steps:
  1. Tune xi on a 1-year out-of-sample slice, logging the FULL curve.
  2. Test the optional ``elo_sum`` feature; keep it only if it improves the
     held-out log-likelihood.
  3. Refit the final model on the whole feature era, fit rho by MLE.
  4. Assert coefficient signs (elo_diff > 0, is_home > 0, rho < 0) before exit.

Artifacts:
  data/processed/model.json       fitted params / xi / rho / features
  reports/xi_tuning.csv           full xi tuning curve(s)
  reports/figures/xi_tuning.png   curve plot

Run from the repo root: ``python scripts/02_fit_model.py``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from wcmodel import data, model  # noqa: E402

REPORTS = data.ROOT / "reports"
FIGURES = REPORTS / "figures"


def main(t: data.Tournament = data.QATAR2022) -> None:
    REPORTS.mkdir(exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    pfx = "" if t.key == "qatar2022" else f"{t.key}_"
    print(f"=== Fitting model for {t.name} (freeze {t.freeze:%Y-%m-%d}) ===\n")

    df = pd.read_parquet(t.proc_dir / "team_match.parquet")
    data.assert_no_leakage(df, t)
    cutoff = t.freeze
    val_cutoff = cutoff - pd.DateOffset(years=1)

    xi_grid = np.round(np.arange(0.0, 0.0105, 0.0005), 5)
    base = ["elo_diff", "is_home"]
    withsum = ["elo_diff", "is_home", "elo_sum"]

    print(f"Feature-era rows: {len(df):,}  ({df.date.min():%Y-%m-%d} -> {df.date.max():%Y-%m-%d})")
    print(f"Validation slice: ({val_cutoff:%Y-%m-%d}, {cutoff:%Y-%m-%d}]\n")

    # --- 1. xi tuning, full curve, for both feature sets -------------------- #
    tune_base = model.tune_xi(df, base, xi_grid, val_cutoff, cutoff)
    tune_sum = model.tune_xi(df, withsum, xi_grid, val_cutoff, cutoff)

    print("xi tuning curve (per-row held-out log-likelihood):")
    print(f"{'xi':>8} | {'base':>12} | {'+elo_sum':>12}")
    print("-" * 38)
    for xi, lb, ls in zip(tune_base.curve.xi, tune_base.curve.val_loglik_per_row,
                          tune_sum.curve.val_loglik_per_row):
        mark = "  <- base best" if xi == tune_base.best_xi else ""
        print(f"{xi:>8.4f} | {lb:>12.5f} | {ls:>12.5f}{mark}")

    curve_out = pd.DataFrame(
        {
            "xi": tune_base.curve.xi,
            "val_loglik_base": tune_base.curve.val_loglik_per_row,
            "val_loglik_elo_sum": tune_sum.curve.val_loglik_per_row,
        }
    )
    curve_out.to_csv(REPORTS / f"{pfx}xi_tuning.csv", index=False)

    # --- 2. keep elo_sum only if it helps out-of-sample --------------------- #
    use_sum = tune_sum.best_loglik > tune_base.best_loglik
    features = withsum if use_sum else base
    best_xi = tune_sum.best_xi if use_sum else tune_base.best_xi
    print(
        f"\nBest held-out LL  base={tune_base.best_loglik:.5f} (xi={tune_base.best_xi}) | "
        f"+elo_sum={tune_sum.best_loglik:.5f} (xi={tune_sum.best_xi})"
    )
    print(
        f"Decision: {'KEEP' if use_sum else 'DROP'} elo_sum "
        f"-> features={features}, xi={best_xi}"
    )

    # --- plot the curve(s) -------------------------------------------------- #
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(tune_base.curve.xi, tune_base.curve.val_loglik_per_row, "o-", label="elo_diff + is_home")
    ax.plot(tune_sum.curve.xi, tune_sum.curve.val_loglik_per_row, "s--", label="+ elo_sum")
    ax.axvline(best_xi, color="grey", ls=":", lw=1)
    ax.set_xlabel("xi (time-decay rate, per day)")
    ax.set_ylabel("held-out Poisson log-likelihood / row")
    ax.set_title(f"{t.name}: xi tuning curve (1-year out-of-sample slice)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / f"{pfx}xi_tuning.png", dpi=120)
    half_life = np.log(2) / best_xi if best_xi > 0 else float("inf")
    print(f"Implied half-life at xi={best_xi}: {half_life:.0f} days (~{half_life/365:.1f} yr)")

    # --- 3. final fit on the whole feature era ------------------------------ #
    fitted = model.fit_model(df, features=features, xi=best_xi, cutoff=cutoff)
    fitted.xi_curve = curve_out

    print("\nFinal GLM coefficients:")
    for name, val in fitted.params.items():
        print(f"  {name:<10} {val:+.4f}")
    print(f"  rho        {fitted.rho:+.4f}")

    # --- 4. sign-assertion gate (PRD M3 DoD) -------------------------------- #
    fitted.assert_sane()
    print("\nSign gate PASSED: elo_diff > 0, is_home > 0, rho < 0.")

    # --- eyeball gate: predicted lambdas for known fixtures ----------------- #
    el = pd.read_parquet(t.proc_dir / "elo_history.parquet")
    snap = (
        el[el.date < cutoff].sort_values("date").groupby("team")["rating_post_match"].last()
    )
    print("\nEyeball gate (predicted λ, neutral venue):")
    print(f"  {'fixture':<26}{'λ_home':>8}{'λ_away':>8}{'total':>8}{'ratio':>8}")
    for h, a in t.eyeball:
        if h not in snap.index or a not in snap.index:
            continue  # a wrong guess is harmless; just skip
        lam_h, lam_a = fitted.fixture_lambdas(snap, h, a, neutral=True)
        print(f"  {h+' - '+a:<26}{lam_h:>8.2f}{lam_a:>8.2f}{lam_h+lam_a:>8.2f}{lam_h/lam_a:>8.1f}")

    out = {
        "features": fitted.features,
        "params": {k: float(v) for k, v in fitted.params.items()},
        "xi": fitted.xi,
        "rho": fitted.rho,
        "cutoff": str(cutoff.date()),
        "val_cutoff": str(val_cutoff.date()),
        "use_elo_sum": bool(use_sum),
        "half_life_days": float(half_life),
    }
    (t.proc_dir / "model.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {(t.proc_dir / 'model.json').relative_to(data.ROOT)}, "
          f"reports/{pfx}xi_tuning.csv, figures/{pfx}xi_tuning.png")


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "qatar2022"
    main(data.TOURNAMENTS[key])
