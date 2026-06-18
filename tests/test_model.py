"""Model tests (M3): weights, Dixon-Coles tau/rho, GLM sign recovery."""

import numpy as np
import pandas as pd
import pytest

from wcmodel import data, model


# --------------------------------------------------------------------------- #
# Sample-weight components
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "tournament, expected",
    [
        ("Friendly", 0.5),
        ("FIFA World Cup qualification", 0.9),
        ("UEFA Euro qualification", 0.9),
        ("FIFA World Cup", 1.0),
        ("UEFA Euro", 1.0),
        ("Copa América", 1.0),
        ("King's Cup", 0.7),
    ],
)
def test_competition_weight(tournament, expected):
    assert model.competition_weight(tournament) == expected


def test_covid_weight_window():
    assert model.covid_weight(pd.Timestamp("2020-09-01")) == 0.7
    assert model.covid_weight(pd.Timestamp("2019-12-31")) == 1.0
    assert model.covid_weight(pd.Timestamp("2021-07-01")) == 1.0


def test_time_weight_scalar_and_series():
    cutoff = pd.Timestamp("2022-11-19")
    # 0 days before cutoff -> weight 1.
    assert model.time_weight(cutoff, cutoff, 0.002) == pytest.approx(1.0)
    s = pd.Series(pd.to_datetime(["2022-11-19", "2021-11-19"]))
    w = model.time_weight(s, cutoff, 0.001)
    assert w[0] == pytest.approx(1.0)
    assert w[1] == pytest.approx(np.exp(-0.001 * 365))


# --------------------------------------------------------------------------- #
# Dixon-Coles tau
# --------------------------------------------------------------------------- #
def test_dixon_coles_tau_cells():
    lam, mu, rho = 1.5, 1.2, -0.1
    assert model.dixon_coles_tau(0, 0, lam, mu, rho) == pytest.approx(1 - lam * mu * rho)
    assert model.dixon_coles_tau(0, 1, lam, mu, rho) == pytest.approx(1 + lam * rho)
    assert model.dixon_coles_tau(1, 0, lam, mu, rho) == pytest.approx(1 + mu * rho)
    assert model.dixon_coles_tau(1, 1, lam, mu, rho) == pytest.approx(1 - rho)
    assert model.dixon_coles_tau(2, 3, lam, mu, rho) == pytest.approx(1.0)


def test_tau_unity_when_rho_zero():
    grid = [(x, y) for x in range(4) for y in range(4)]
    for x, y in grid:
        assert model.dixon_coles_tau(x, y, 1.3, 1.1, 0.0) == pytest.approx(1.0)


# --------------------------------------------------------------------------- #
# rho MLE recovers a negative value when low scores are over-represented
# --------------------------------------------------------------------------- #
def test_fit_rho_negative_on_draw_heavy_data():
    # Many 0-0 and 1-1, few 0-1/1-0: with lam=mu=1, tau favours rho < 0.
    scores = [(0, 0)] * 30 + [(1, 1)] * 60 + [(0, 1)] * 5 + [(1, 0)] * 5
    rows = []
    for mid, (x, y) in enumerate(scores):
        rows.append({"match_id": mid, "side": "home", "goals_for": x})
        rows.append({"match_id": mid, "side": "away", "goals_for": y})
    df = pd.DataFrame(rows)
    lam = np.ones(len(df))
    rho = model.fit_rho(df, lam)
    assert rho < 0


# --------------------------------------------------------------------------- #
# GLM recovers the expected coefficient signs on synthetic data
# --------------------------------------------------------------------------- #
def _synthetic_team_match(n=4000, seed=1):
    rng = np.random.default_rng(seed)
    team_elo = rng.normal(1500, 150, n)
    opp_elo = rng.normal(1500, 150, n)
    is_home = rng.integers(0, 2, n)
    eta = 0.0 + 0.8 * (team_elo - opp_elo) / 400 + 0.3 * is_home
    goals = rng.poisson(np.exp(eta))
    return pd.DataFrame(
        {
            "date": pd.Timestamp("2010-01-01") + pd.to_timedelta(rng.integers(0, 3000, n), "D"),
            "team_elo_pre": team_elo,
            "opp_elo_pre": opp_elo,
            "is_home": is_home,
            "goals_for": goals,
            "tournament": "Friendly",
        }
    )


def test_glm_sign_recovery():
    df = _synthetic_team_match()
    fit = model.fit_glm(df, xi=0.0, features=["elo_diff", "is_home"], cutoff=df.date.max())
    params = pd.Series(fit.params, index=["intercept", "elo_diff", "is_home"])
    assert params["elo_diff"] > 0
    assert params["is_home"] > 0
    # Roughly recovers the generating coefficients.
    assert params["elo_diff"] == pytest.approx(0.8, abs=0.15)
    assert params["is_home"] == pytest.approx(0.3, abs=0.15)


def test_fit_glm_rejects_leakage():
    df = _synthetic_team_match(n=100)
    with pytest.raises(AssertionError):
        model.fit_glm(df, xi=0.0, features=["elo_diff"], cutoff=df.date.min())


# --------------------------------------------------------------------------- #
# End-to-end on the real feature table: the sign gate must pass
# --------------------------------------------------------------------------- #
def test_real_model_passes_sign_gate():
    path = data.PROCESSED / "team_match.parquet"
    if not path.exists():
        pytest.skip("team_match.parquet not built; run scripts/01_build_data.py")
    df = pd.read_parquet(path)
    # Fixed xi (no tuning) keeps this fast; we only assert the gate here.
    fitted = model.fit_model(df, features=["elo_diff", "is_home"], xi=0.002)
    fitted.assert_sane()


# --------------------------------------------------------------------------- #
# v2 goal_scale: applied at prediction time only, persisted, 1X2 ratio ~fixed
# --------------------------------------------------------------------------- #
def _toy_model(goal_scale=1.0):
    return model.FittedModel(
        features=["elo_diff", "is_home"],
        params=pd.Series({"intercept": 0.05, "elo_diff": 0.77, "is_home": 0.25}),
        xi=0.0015, rho=-0.05, goal_scale=goal_scale,
    )


def test_goal_scale_scales_fixture_lambdas():
    ratings = pd.Series({"A": 1800.0, "B": 1500.0})
    lam1, mu1 = _toy_model(1.0).fixture_lambdas(ratings, "A", "B", neutral=True)
    lam2, mu2 = _toy_model(1.1).fixture_lambdas(ratings, "A", "B", neutral=True)
    assert lam2 == pytest.approx(1.1 * lam1)
    assert mu2 == pytest.approx(1.1 * mu1)


def test_goal_scale_default_is_one_and_roundtrips():
    assert _toy_model().goal_scale == 1.0
    m2 = model.FittedModel.from_dict(_toy_model(1.1).to_dict())
    assert m2.goal_scale == 1.1
    # v1 JSON without the key loads as 1.0 (backward compatible)
    d = _toy_model().to_dict()
    del d["goal_scale"]
    assert model.FittedModel.from_dict(d).goal_scale == 1.0
