"""Elo engine sanity tests (M2)."""

import numpy as np
import pandas as pd
import pytest

from wcmodel import elo


# --------------------------------------------------------------------------- #
# K-factor tiers
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "tournament, expected",
    [
        ("Friendly", 20.0),
        ("FIFA World Cup qualification", 40.0),
        ("UEFA Euro qualification", 40.0),
        ("FIFA World Cup", 60.0),
        ("UEFA Euro", 50.0),
        ("Copa América", 50.0),
        ("Confederations Cup", 50.0),
        ("UEFA Nations League", 50.0),
        ("Gold Cup", 50.0),
        ("King's Cup", 30.0),  # minor tournament
    ],
)
def test_k_factor(tournament, expected):
    assert elo.k_factor(tournament) == expected


# --------------------------------------------------------------------------- #
# Goal-difference multiplier
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "gd, expected",
    [
        (0, 1.0),
        (1, 1.0),
        (2, 1.5),
        (3, 1.75),
        (4, 1.875),  # 1.75 + 1/8
        (5, 2.0),  # 1.75 + 2/8
    ],
)
def test_gd_multiplier(gd, expected):
    assert elo.gd_multiplier(gd) == pytest.approx(expected)


# --------------------------------------------------------------------------- #
# Expectancy
# --------------------------------------------------------------------------- #
def test_expectancy_equal_no_home():
    assert elo.expectancy(1500, 1500, 0.0) == pytest.approx(0.5)


def test_expectancy_home_bonus_helps():
    assert elo.expectancy(1500, 1500, 100.0) > 0.5


def test_expectancy_complementary():
    # Home expectancy (with bonus) + away expectancy (seeing -bonus) == 1.
    we_home = elo.expectancy(1600, 1500, 100.0)
    we_away = elo.expectancy(1500, 1600, -100.0)
    assert we_home + we_away == pytest.approx(1.0)


def test_expectancy_known_400_gap():
    # A 400-point edge -> ~10:1 expectancy.
    assert elo.expectancy(1900, 1500, 0.0) == pytest.approx(10 / 11, abs=1e-9)


# --------------------------------------------------------------------------- #
# A single hand-computed match
# --------------------------------------------------------------------------- #
def test_single_match_update():
    matches = pd.DataFrame(
        {
            "date": pd.to_datetime(["2000-01-01"]),
            "home_team": ["A"],
            "away_team": ["B"],
            "home_score": [1],
            "away_score": [0],
            "tournament": ["Friendly"],
            "neutral": [True],  # no home bonus
        }
    )
    out = elo.compute_elo(matches)
    # K=20, mult=1, we_home=0.5, delta = 20 * (1 - 0.5) = 10.
    home_row = out[out.team == "A"].iloc[0]
    away_row = out[out.team == "B"].iloc[0]
    assert home_row.team_elo_pre == pytest.approx(1500.0)
    assert home_row.team_elo_post == pytest.approx(1510.0)
    assert away_row.team_elo_post == pytest.approx(1490.0)


def test_home_bonus_changes_update():
    base = dict(
        date=pd.to_datetime(["2000-01-01"]),
        home_team=["A"],
        away_team=["B"],
        home_score=[1],
        away_score=[0],
        tournament=["Friendly"],
    )
    neutral = elo.compute_elo(pd.DataFrame({**base, "neutral": [True]}))
    at_home = elo.compute_elo(pd.DataFrame({**base, "neutral": [False]}))
    # With the +100 bonus the win is "more expected", so A gains fewer points.
    gain_neutral = neutral[neutral.team == "A"].iloc[0].team_elo_post - 1500
    gain_home = at_home[at_home.team == "A"].iloc[0].team_elo_post - 1500
    assert gain_home < gain_neutral


# --------------------------------------------------------------------------- #
# Structural invariants over a synthetic sweep
# --------------------------------------------------------------------------- #
def _synthetic_matches(n=200, seed=0):
    rng = np.random.default_rng(seed)
    teams = [f"T{i}" for i in range(8)]
    rows = []
    for d in range(n):
        h, a = rng.choice(teams, size=2, replace=False)
        rows.append(
            {
                "date": pd.Timestamp("2000-01-01") + pd.Timedelta(days=d),
                "home_team": h,
                "away_team": a,
                "home_score": int(rng.integers(0, 4)),
                "away_score": int(rng.integers(0, 4)),
                "tournament": "Friendly",
                "neutral": bool(rng.integers(0, 2)),
            }
        )
    return pd.DataFrame(rows)


def test_zero_sum_conservation():
    m = _synthetic_matches()
    out = elo.compute_elo(m)
    # Total rating is conserved: every delta is added to one side, removed from
    # the other. Final total == initial total over all teams that played.
    final = elo.latest_ratings(out, as_of=m.date.max() + pd.Timedelta(days=1))
    n_teams = len(set(m.home_team) | set(m.away_team))
    assert final.sum() == pytest.approx(elo.INITIAL_RATING * n_teams, abs=1e-6)


def test_two_rows_per_match_and_pre_carries_forward():
    m = _synthetic_matches(n=50)
    out = elo.compute_elo(m)
    assert len(out) == 2 * len(m)
    # For an arbitrary team, each match's pre rating equals the previous post.
    team = "T0"
    seq = out[out.team == team].sort_values("date")
    posts = seq.team_elo_post.to_numpy()
    pres = seq.team_elo_pre.to_numpy()
    assert np.allclose(pres[1:], posts[:-1])


def test_burn_in_skips_early_matches():
    m = pd.DataFrame(
        {
            "date": pd.to_datetime(["1990-01-01", "2000-01-01"]),
            "home_team": ["A", "A"],
            "away_team": ["B", "B"],
            "home_score": [5, 1],
            "away_score": [0, 0],
            "tournament": ["Friendly", "Friendly"],
            "neutral": [True, True],
        }
    )
    out = elo.compute_elo(m, burn_in_start=pd.Timestamp("1993-01-01"))
    # The 1990 thrashing is before burn-in: A still starts the 2000 match at 1500.
    assert out.iloc[0].team_elo_pre == pytest.approx(1500.0)
