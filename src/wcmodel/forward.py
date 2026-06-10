"""Shared helpers for forward (current-Elo) prediction of upcoming fixtures.

Used by both ``scripts/predict_fixtures.py`` and ``scripts/report_upcoming.py``:
load the schedule, compute current Elo from all played matches, and select each
team's next unplayed match (the "matchday" that drives the update-as-you-go loop).
"""

from __future__ import annotations

import urllib.request

import pandas as pd

from . import elo
from .data import RAW_RESULTS, ROOT, normalize_team

RESULTS_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
WC_TOURNAMENT = "FIFA World Cup"


def refresh_snapshot() -> None:
    """Re-download the results snapshot so new results feed current Elo."""
    print(f"Refreshing snapshot from {RESULTS_URL} ...")
    urllib.request.urlretrieve(RESULTS_URL, RAW_RESULTS)
    print(f"  wrote {RAW_RESULTS.relative_to(ROOT)}")


def load_schedule() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (played, upcoming_wc) frames with normalized team names."""
    raw = pd.read_csv(RAW_RESULTS)
    raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
    raw = raw.dropna(subset=["date"])
    raw["home_team"] = raw["home_team"].map(normalize_team)
    raw["away_team"] = raw["away_team"].map(normalize_team)
    if raw["neutral"].dtype == object:
        raw["neutral"] = raw["neutral"].astype(str).str.upper().map(
            {"TRUE": True, "FALSE": False}
        )
    raw["neutral"] = raw["neutral"].astype(bool)

    played = raw.dropna(subset=["home_score", "away_score"]).copy()
    upcoming = raw[
        (raw["tournament"] == WC_TOURNAMENT) & (raw["home_score"].isna())
    ].sort_values("date", kind="mergesort").reset_index(drop=True)
    return played, upcoming


def next_round(upcoming: pd.DataFrame) -> pd.DataFrame:
    """Each team's next unplayed match: greedy over date order.

    A match is included iff neither team has already been claimed by an earlier
    match. On a full group stage this returns exactly the next matchday.
    """
    seen: set[str] = set()
    keep = []
    for fx in upcoming.itertuples(index=False):
        if fx.home_team in seen or fx.away_team in seen:
            continue
        keep.append(fx)
        seen.update([fx.home_team, fx.away_team])
    return pd.DataFrame(keep)


def current_ratings(played: pd.DataFrame) -> tuple[pd.Series, pd.Timestamp]:
    """Latest Elo per team from all played matches (no freeze)."""
    elo_long = elo.compute_elo(played.sort_values("date", kind="mergesort"))
    as_of = played["date"].max()
    return elo.latest_ratings(elo_long, as_of + pd.Timedelta(days=1)), as_of
