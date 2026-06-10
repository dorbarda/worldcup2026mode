"""Goal-expectation model: weighted Poisson GLM + Dixon-Coles dependence.

Two pieces, fit in order:

1. **Poisson GLM (log link)** on team-match rows, predicting goals scored from
   the Elo difference and a home-advantage term::

       goals_scored ~ intercept + elo_diff + is_home   [+ elo_sum]

   with multiplicative sample weights: a time-decay term ``exp(-xi*days)``, a
   competition-importance weight, and a COVID empty-stadium down-weight.

2. **Dixon-Coles rho** correction, fit by maximum likelihood *after* the GLM,
   coupling the four low-score cells of each match's joint distribution.

The time-decay rate ``xi`` is tuned by maximizing out-of-sample log-likelihood
on a held-out validation slice (see :func:`tune_xi`).

Leakage discipline: every fit asserts its training rows fall on or before the
supplied cutoff.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import minimize_scalar
from scipy.stats import poisson

from .data import FEATURE_START, FREEZE_DATE
from .elo import _CONTINENTAL_FINALS

# --------------------------------------------------------------------------- #
# Sample-weight components
# --------------------------------------------------------------------------- #
COVID_START = pd.Timestamp("2020-03-01")
COVID_END = pd.Timestamp("2021-06-30")
COVID_WEIGHT = 0.7

# Elo-sum is centred so that two average (1500) teams give 0.
_ELO_SUM_CENTER = 3000.0


def competition_weight(tournament: str) -> float:
    """Importance weight for a competition (PRD 4.1)."""
    t = str(tournament).lower()
    if t == "friendly":
        return 0.5
    if "qualification" in t or "qualifier" in t:
        return 0.9
    if t == "fifa world cup" or any(name in t for name in _CONTINENTAL_FINALS):
        return 1.0
    return 0.7  # other tournaments


def covid_weight(date: pd.Timestamp) -> float:
    """Down-weight empty-stadium matches that distorted home advantage."""
    return COVID_WEIGHT if COVID_START <= date <= COVID_END else 1.0


def time_weight(date: pd.Series | pd.Timestamp, cutoff: pd.Timestamp, xi: float):
    """Exponential time decay ``exp(-xi * days_before_cutoff)``."""
    days = (cutoff - pd.to_datetime(date)).dt.days if hasattr(date, "dt") else (
        cutoff - date
    ).days
    return np.exp(-xi * np.asarray(days, dtype=float))


# --------------------------------------------------------------------------- #
# Design matrix
# --------------------------------------------------------------------------- #
def elo_diff(df: pd.DataFrame) -> pd.Series:
    return (df["team_elo_pre"] - df["opp_elo_pre"]) / 400.0


def elo_sum(df: pd.DataFrame) -> pd.Series:
    return (df["team_elo_pre"] + df["opp_elo_pre"] - _ELO_SUM_CENTER) / 400.0


def build_design(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    """Construct the GLM design matrix for the requested feature set."""
    cols = {"intercept": np.ones(len(df))}
    if "elo_diff" in features:
        cols["elo_diff"] = elo_diff(df).to_numpy()
    if "is_home" in features:
        cols["is_home"] = df["is_home"].to_numpy(dtype=float)
    if "elo_sum" in features:
        cols["elo_sum"] = elo_sum(df).to_numpy()
    return pd.DataFrame(cols, index=df.index)


def sample_weights(df: pd.DataFrame, cutoff: pd.Timestamp, xi: float) -> np.ndarray:
    """Multiplicative sample weights: time decay x competition x COVID."""
    w_time = time_weight(df["date"], cutoff, xi)
    w_comp = df["tournament"].map(competition_weight).to_numpy(dtype=float)
    w_covid = df["date"].map(covid_weight).to_numpy(dtype=float)
    return w_time * w_comp * w_covid


# --------------------------------------------------------------------------- #
# GLM fit / predict
# --------------------------------------------------------------------------- #
def fit_glm(
    df: pd.DataFrame,
    xi: float,
    features: list[str],
    cutoff: pd.Timestamp = FREEZE_DATE,
) -> sm.GLM:
    """Fit the weighted Poisson GLM on team-match rows dated <= ``cutoff``."""
    assert df["date"].max() <= cutoff, "leakage: training rows after cutoff"
    X = build_design(df, features)
    y = df["goals_for"].to_numpy(dtype=float)
    w = sample_weights(df, cutoff, xi)
    model = sm.GLM(y, X, family=sm.families.Poisson(), freq_weights=w)
    return model.fit()


def predict_lambda(fit: sm.GLM, df: pd.DataFrame, features: list[str]) -> np.ndarray:
    """Predicted goal expectation (lambda) for each team-match row."""
    X = build_design(df, features)
    return np.asarray(fit.predict(X), dtype=float)


# --------------------------------------------------------------------------- #
# xi tuning (out-of-sample)
# --------------------------------------------------------------------------- #
def _poisson_loglik(y: np.ndarray, lam: np.ndarray) -> float:
    return float(poisson.logpmf(y, lam).sum())


def tune_xi(
    df: pd.DataFrame,
    features: list[str],
    grid: np.ndarray,
    val_cutoff: pd.Timestamp,
    cutoff: pd.Timestamp = FREEZE_DATE,
) -> "XiTuning":
    """Pick ``xi`` by out-of-sample log-likelihood on a held-out slice.

    For each candidate ``xi``: fit the GLM on rows dated <= ``val_cutoff`` (decay
    measured to ``val_cutoff``), then score the marginal Poisson log-likelihood
    on the held-out rows in ``(val_cutoff, cutoff]``. The full curve is returned,
    not just the argmax.
    """
    train = df[df["date"] <= val_cutoff]
    val = df[(df["date"] > val_cutoff) & (df["date"] <= cutoff)]
    y_val = val["goals_for"].to_numpy(dtype=float)

    curve = []
    for xi in grid:
        fit = fit_glm(train, xi=float(xi), features=features, cutoff=val_cutoff)
        lam = predict_lambda(fit, val, features)
        ll = _poisson_loglik(y_val, lam)
        curve.append((float(xi), ll / len(val)))  # per-row mean log-likelihood

    curve_df = pd.DataFrame(curve, columns=["xi", "val_loglik_per_row"])
    best = curve_df.loc[curve_df["val_loglik_per_row"].idxmax()]
    return XiTuning(
        curve=curve_df,
        best_xi=float(best["xi"]),
        best_loglik=float(best["val_loglik_per_row"]),
        n_val=len(val),
        val_cutoff=val_cutoff,
    )


@dataclass
class XiTuning:
    curve: pd.DataFrame
    best_xi: float
    best_loglik: float
    n_val: int
    val_cutoff: pd.Timestamp


# --------------------------------------------------------------------------- #
# Dixon-Coles dependence
# --------------------------------------------------------------------------- #
def dixon_coles_tau(x, y, lam, mu, rho):
    """Low-score dependence factor tau(x, y). Scalar or array inputs."""
    x = np.asarray(x)
    y = np.asarray(y)
    tau = np.ones(np.broadcast(x, y, lam, mu).shape, dtype=float)
    tau = np.where((x == 0) & (y == 0), 1.0 - lam * mu * rho, tau)
    tau = np.where((x == 0) & (y == 1), 1.0 + lam * rho, tau)
    tau = np.where((x == 1) & (y == 0), 1.0 + mu * rho, tau)
    tau = np.where((x == 1) & (y == 1), 1.0 - rho, tau)
    return tau


def _match_level(df: pd.DataFrame, lam: np.ndarray) -> pd.DataFrame:
    """Pivot team-match rows + predicted lambdas to one row per match."""
    tmp = df[["match_id", "side", "goals_for"]].copy()
    tmp["lam"] = lam
    home = tmp[tmp["side"] == "home"].set_index("match_id")
    away = tmp[tmp["side"] == "away"].set_index("match_id")
    return pd.DataFrame(
        {
            "lam": home["lam"],          # home expected goals
            "mu": away["lam"],           # away expected goals
            "x": home["goals_for"],      # actual home goals
            "y": away["goals_for"],      # actual away goals
        }
    ).dropna()


def fit_rho(df: pd.DataFrame, lam: np.ndarray, bounds=(-0.2, 0.2)) -> float:
    """MLE of the Dixon-Coles rho given fixed per-row lambdas."""
    m = _match_level(df, lam)
    lam_h = m["lam"].to_numpy()
    mu_a = m["mu"].to_numpy()
    x = m["x"].to_numpy()
    y = m["y"].to_numpy()

    def negll(rho: float) -> float:
        tau = dixon_coles_tau(x, y, lam_h, mu_a, rho)
        if np.any(tau <= 0):
            return 1e12
        return -float(np.sum(np.log(tau)))  # Poisson terms are constant in rho

    res = minimize_scalar(negll, bounds=bounds, method="bounded")
    return float(res.x)


# --------------------------------------------------------------------------- #
# End-to-end fitted model
# --------------------------------------------------------------------------- #
@dataclass
class FittedModel:
    features: list[str]
    params: pd.Series
    xi: float
    rho: float
    cutoff: pd.Timestamp = FREEZE_DATE
    xi_curve: pd.DataFrame | None = field(default=None, repr=False)

    def predict_lambdas(
        self, df_or_features: pd.DataFrame, *, is_home: np.ndarray | None = None
    ) -> np.ndarray:
        """Predict lambda for team-match rows (needs team_elo_pre/opp_elo_pre/is_home)."""
        X = build_design(df_or_features, self.features)
        eta = X.to_numpy() @ self.params[X.columns].to_numpy()
        return np.exp(eta)

    def assert_sane(self) -> None:
        """Coefficient-sign sanity gate (PRD M3 definition of done)."""
        if self.params.get("elo_diff", 0.0) <= 0:
            raise AssertionError(f"elo_diff coef must be > 0, got {self.params.get('elo_diff')}")
        if self.params.get("is_home", 0.0) <= 0:
            raise AssertionError(f"is_home coef must be > 0, got {self.params.get('is_home')}")
        if self.rho >= 0:
            raise AssertionError(f"Dixon-Coles rho must be < 0, got {self.rho}")


def fit_model(
    df: pd.DataFrame,
    features: list[str] = ("elo_diff", "is_home"),
    xi: float | None = None,
    xi_grid: np.ndarray | None = None,
    val_cutoff: pd.Timestamp | None = None,
    cutoff: pd.Timestamp = FREEZE_DATE,
) -> FittedModel:
    """Fit the full model: tune xi (if not given), fit GLM, then fit rho.

    ``df`` is the feature-era team-match table (>= 2000), dated <= ``cutoff``.
    """
    features = list(features)
    assert df["date"].max() <= cutoff, "leakage: feature rows after cutoff"

    tuning = None
    if xi is None:
        if xi_grid is None:
            xi_grid = np.round(np.arange(0.0, 0.0105, 0.0005), 5)
        if val_cutoff is None:
            val_cutoff = cutoff - pd.DateOffset(years=1)
        tuning = tune_xi(df, features, xi_grid, val_cutoff, cutoff)
        xi = tuning.best_xi

    fit = fit_glm(df, xi=xi, features=features, cutoff=cutoff)
    params = pd.Series(fit.params, index=build_design(df.head(1), features).columns)
    lam = predict_lambda(fit, df, features)
    rho = fit_rho(df, lam)

    return FittedModel(
        features=features,
        params=params,
        xi=float(xi),
        rho=rho,
        cutoff=cutoff,
        xi_curve=None if tuning is None else tuning.curve,
    )
