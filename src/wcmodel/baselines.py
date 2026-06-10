"""Backtest baselines B0-B3 (PRD 5.3).

Each baseline produces a 1X2 probability stack ``(n, 3)`` aligned to the test
fixtures, with outcome order [home, draw, away]. B0 also yields exact-score
matrices (so it gets a log-loss column); the others are 1X2-only.

* B0 Naive       -- every match lambda = 1.35 / 1.35.
* B1 Elo-only    -- multinomial logit of outcome on the home-adjusted Elo
                    difference, fit on the training set.
* B2 Market      -- de-vigged closing 1X2 odds (external CSV; N/A if absent).
* B3 538         -- archived FiveThirtyEight WC-2022 forecasts (external CSV;
                    N/A if absent -- the live API host is offline / blocked).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from . import matrix as mx
from .data import DATA

HOME_ADV = 100.0  # Elo home bonus used by B1 expectancy
NAIVE_LAMBDA = 1.35


# --------------------------------------------------------------------------- #
# B0 -- Naive
# --------------------------------------------------------------------------- #
def b0_naive(n_fixtures: int, rho: float = 0.0):
    """Identical 1.35/1.35 prediction for every fixture.

    Returns (probs (n,3), matrix) -- the matrix is shared since every fixture is
    the same, and feeds the exact-score log loss.
    """
    M = mx.score_matrix(NAIVE_LAMBDA, NAIVE_LAMBDA, rho)
    d = mx.derived_markets(M)
    row = np.array([d["p_home"], d["p_draw"], d["p_away"]])
    probs = np.tile(row, (n_fixtures, 1))
    return probs, M


# --------------------------------------------------------------------------- #
# B1 -- Elo-only multinomial logit
# --------------------------------------------------------------------------- #
def _home_adjusted_dr(home_elo, away_elo, neutral) -> np.ndarray:
    bonus = np.where(np.asarray(neutral), 0.0, HOME_ADV)
    return (np.asarray(home_elo) - np.asarray(away_elo) + bonus) / 400.0


def fit_b1(team_match: pd.DataFrame):
    """Fit a multinomial logit of 1X2 outcome on home-adjusted Elo diff.

    Uses the home-side rows of the feature-era team-match table as match rows.
    Returns a fitted statsmodels MNLogit result.
    """
    import statsmodels.api as sm

    home = team_match[team_match["side"] == "home"].copy()
    dr = (home["team_elo_pre"] - home["opp_elo_pre"] + HOME_ADV * home["is_home"]) / 400.0
    # outcome: 0 home win, 1 draw, 2 away win
    y = np.where(
        home["goals_for"] > home["goals_against"], 0,
        np.where(home["goals_for"] == home["goals_against"], 1, 2),
    )
    X = sm.add_constant(pd.DataFrame({"dr": dr.to_numpy()}))
    return sm.MNLogit(y, X).fit(disp=False)


def b1_elo_only(fit, home_elo, away_elo, neutral) -> np.ndarray:
    """Predict 1X2 for fixtures from the fitted B1 model."""
    import statsmodels.api as sm

    dr = _home_adjusted_dr(home_elo, away_elo, neutral)
    X = sm.add_constant(pd.DataFrame({"dr": dr}), has_constant="add")
    return np.asarray(fit.predict(X))  # columns already [home, draw, away]


# --------------------------------------------------------------------------- #
# B2 / B3 -- external sources (de-vig / archived forecasts)
# --------------------------------------------------------------------------- #
def _devig(odds_home, odds_draw, odds_away) -> np.ndarray:
    raw = np.array([1 / odds_home, 1 / odds_draw, 1 / odds_away], dtype=float)
    return raw / raw.sum()


def load_market(test_fixtures: pd.DataFrame, path: Path | None = None):
    """B2: de-vigged closing 1X2 odds aligned to fixtures, or None if unavailable.

    Expected CSV columns: home_team, away_team, odds_home, odds_draw, odds_away.
    """
    path = path or (DATA / "external" / "qatar2022_closing_odds.csv")
    if not Path(path).exists():
        return None
    odds = pd.read_csv(path)
    merged = test_fixtures.merge(odds, on=["home_team", "away_team"], how="left")
    if merged[["odds_home", "odds_draw", "odds_away"]].isna().any().any():
        return None
    return np.vstack(
        [_devig(r.odds_home, r.odds_draw, r.odds_away) for r in merged.itertuples()]
    )


def load_538(test_fixtures: pd.DataFrame, path: Path | None = None):
    """B3: archived 538 WC-2022 1X2 forecasts aligned to fixtures, or None.

    Expected CSV columns: home_team, away_team, prob_home, prob_draw, prob_away.
    """
    path = path or (DATA / "external" / "fivethirtyeight_wc2022.csv")
    if not Path(path).exists():
        return None
    f = pd.read_csv(path)
    merged = test_fixtures.merge(f, on=["home_team", "away_team"], how="left")
    cols = ["prob_home", "prob_draw", "prob_away"]
    if merged[cols].isna().any().any():
        return None
    p = merged[cols].to_numpy(dtype=float)
    return p / p.sum(axis=1, keepdims=True)
