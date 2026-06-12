"""As-of-date Elo engine, following eloratings.net conventions.

We rebuild Elo from the results dataset rather than scraping, because we need
the rating each team held *on each match date* (the ``rating_pre_match``), and
because a recomputed history is fully reproducible.

Conventions (per the PRD / eloratings.net):

* All teams start at 1500.
* K-factor by competition: World Cup 60, continental finals / Confederations 50,
  qualifiers 40, other tournaments 30, friendlies 20.
* Goal-difference multiplier: win by 2 -> x1.5, by 3 -> x1.75,
  by N>=4 -> x(1.75 + (N-3)/8).
* Home advantage: +100 Elo to the home side in the expectancy calc, but 0 when
  the match is played on neutral ground.
* Expectancy: ``W_e = 1 / (10**(-dr/400) + 1)`` with ``dr`` the rating diff
  including the home bonus.
* Updates are zero-sum: the points the winner gains, the loser loses.
* Burn-in from 1960; ratings from 2000+ are what the model trusts as features.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .data import ELO_BURN_IN_START

INITIAL_RATING = 1500.0
HOME_ADVANTAGE = 100.0

# --------------------------------------------------------------------------- #
# Competition K-factors
# --------------------------------------------------------------------------- #
# Continental championship final tournaments + major intercontinental cups.
_CONTINENTAL_FINALS = (
    "uefa euro",
    "copa américa",
    "copa america",
    "african cup of nations",
    "afc asian cup",
    "gold cup",
    "concacaf championship",
    "confederations cup",
    "nations league",
    "oceania nations cup",
)


def k_factor(tournament: str) -> float:
    """K-factor for a competition string (eloratings.net tiers)."""
    t = str(tournament).lower()
    if t == "friendly":
        return 20.0
    if "qualification" in t or "qualifier" in t:
        return 40.0
    if t == "fifa world cup":
        return 60.0
    if any(name in t for name in _CONTINENTAL_FINALS):
        return 50.0
    return 30.0  # all other tournaments


def gd_multiplier(goal_diff: int) -> float:
    """Goal-difference multiplier on the K-factor."""
    n = abs(int(goal_diff))
    if n <= 1:
        return 1.0
    if n == 2:
        return 1.5
    if n == 3:
        return 1.75
    return 1.75 + (n - 3) / 8.0  # N >= 4


def expectancy(rating: float, opp_rating: float, home_bonus: float = 0.0) -> float:
    """Expected score (win prob + half draw prob) for ``rating`` vs opponent."""
    dr = (rating + home_bonus) - opp_rating
    return 1.0 / (10.0 ** (-dr / 400.0) + 1.0)


# --------------------------------------------------------------------------- #
# Main sweep
# --------------------------------------------------------------------------- #
def compute_elo(
    matches: pd.DataFrame,
    burn_in_start: pd.Timestamp = ELO_BURN_IN_START,
    initial_rating: float = INITIAL_RATING,
) -> pd.DataFrame:
    """Sweep matches chronologically and produce per-team-match Elo records.

    ``matches`` must have columns: date, home_team, away_team, home_score,
    away_score, tournament, neutral (as produced by :func:`data.load_raw`).

    Returns a long-format frame with two rows per match (home and away),
    columns::

        date, team, opponent, is_home, neutral, tournament,
        goals_for, goals_against,
        team_elo_pre, opp_elo_pre, team_elo_post, k, gd_mult

    ``team_elo_pre`` is the as-of-date rating for that match: exactly the value
    the model is allowed to use as a feature. Matches before ``burn_in_start``
    are skipped (teams simply carry the initial rating into the burn-in).
    """
    matches = matches.sort_values("date", kind="mergesort").reset_index(drop=True)

    ratings: dict[str, float] = {}
    records: list[dict] = []
    match_id = 0

    for row in matches.itertuples(index=False):
        if row.date < burn_in_start:
            continue

        home, away = row.home_team, row.away_team
        r_home = ratings.get(home, initial_rating)
        r_away = ratings.get(away, initial_rating)

        home_bonus = 0.0 if row.neutral else HOME_ADVANTAGE
        we_home = expectancy(r_home, r_away, home_bonus)

        if row.home_score > row.away_score:
            result_home = 1.0
        elif row.home_score < row.away_score:
            result_home = 0.0
        else:
            result_home = 0.5

        gd = abs(row.home_score - row.away_score)
        k = k_factor(row.tournament)
        mult = gd_multiplier(gd)

        delta = k * mult * (result_home - we_home)
        r_home_post = r_home + delta
        r_away_post = r_away - delta  # zero-sum

        ratings[home] = r_home_post
        ratings[away] = r_away_post

        common = {
            "match_id": match_id,
            "date": row.date,
            "neutral": row.neutral,
            "tournament": row.tournament,
            "k": k,
            "gd_mult": mult,
        }
        records.append(
            {
                **common,
                "side": "home",
                "team": home,
                "opponent": away,
                "is_home": 0 if row.neutral else 1,
                "goals_for": row.home_score,
                "goals_against": row.away_score,
                "team_elo_pre": r_home,
                "opp_elo_pre": r_away,
                "team_elo_post": r_home_post,
            }
        )
        records.append(
            {
                **common,
                "side": "away",
                "team": away,
                "opponent": home,
                "is_home": 0,
                "goals_for": row.away_score,
                "goals_against": row.home_score,
                "team_elo_pre": r_away,
                "opp_elo_pre": r_home,
                "team_elo_post": r_away_post,
            }
        )
        match_id += 1

    cols = [
        "match_id",
        "date",
        "side",
        "team",
        "opponent",
        "is_home",
        "neutral",
        "tournament",
        "goals_for",
        "goals_against",
        "team_elo_pre",
        "opp_elo_pre",
        "team_elo_post",
        "k",
        "gd_mult",
    ]
    return pd.DataFrame.from_records(records)[cols]


def elo_history(elo_long: pd.DataFrame) -> pd.DataFrame:
    """Collapse the long Elo frame to (date, team, rating_pre/post_match)."""
    hist = elo_long[["date", "team", "team_elo_pre", "team_elo_post"]].rename(
        columns={"team_elo_pre": "rating_pre_match", "team_elo_post": "rating_post_match"}
    )
    return hist.sort_values(["date", "team"], kind="mergesort").reset_index(drop=True)


def latest_ratings(elo_long: pd.DataFrame, as_of: pd.Timestamp) -> pd.Series:
    """Each team's most recent post-match rating strictly before ``as_of``.

    This is the snapshot used to predict a frozen slate of fixtures (e.g. all
    Qatar 2022 group matches as of the freeze date).
    """
    hist = elo_long.loc[elo_long["date"] < as_of]
    hist = hist.sort_values("date", kind="mergesort")
    return hist.groupby("team")["team_elo_post"].last()


# --------------------------------------------------------------------------- #
# Momentum / form layer (experimental — off by default; not yet backtested)
# --------------------------------------------------------------------------- #
# Competition emphasis for the momentum term: friendlies count for nothing,
# qualifiers some, and finals tournaments fully.
def momentum_weight(tournament: str) -> float:
    t = str(tournament).lower()
    if t == "friendly":
        return 0.0
    if "qualification" in t or "qualifier" in t:
        return 0.6
    if t == "fifa world cup" or any(name in t for name in _CONTINENTAL_FINALS):
        return 1.0
    return 0.3  # other tournaments


def momentum(
    elo_long: pd.DataFrame,
    as_of: pd.Timestamp,
    alpha: float = 0.5,
    half_life_days: float = 270.0,
    cap: float = 60.0,
) -> pd.Series:
    """Per-team form bonus (Elo points) from recent **competitive** results.

    For each team, sum the Elo points won/lost in its matches before ``as_of``,
    weighted by recency (exponential half-life) and competition importance
    (:func:`momentum_weight`; friendlies excluded). The result is scaled by
    ``alpha`` and clipped to +/- ``cap``. This is a *prediction-time* add-on:
    ``effective_rating = base_rating + momentum`` — the stored Elo history is
    untouched, so the bonus is a single tunable knob (alpha=0 turns it off).
    """
    as_of = pd.Timestamp(as_of)
    df = elo_long.loc[elo_long["date"] < as_of]
    if df.empty:
        return pd.Series(dtype=float)
    delta = df["team_elo_post"] - df["team_elo_pre"]
    days = (as_of - df["date"]).dt.days.to_numpy()
    recency = 0.5 ** (days / half_life_days)
    comp = df["tournament"].map(momentum_weight).to_numpy()
    contrib = recency * comp * delta.to_numpy()
    raw = pd.Series(contrib, index=df["team"].to_numpy()).groupby(level=0).sum()
    return (alpha * raw).clip(-cap, cap)


def effective_ratings(
    elo_long: pd.DataFrame, as_of: pd.Timestamp, **momentum_kwargs
) -> pd.Series:
    """Base as-of ratings plus the momentum bonus (0 for teams with no history)."""
    base = latest_ratings(elo_long, as_of)
    bonus = momentum(elo_long, as_of, **momentum_kwargs)
    return base.add(bonus.reindex(base.index).fillna(0.0))
