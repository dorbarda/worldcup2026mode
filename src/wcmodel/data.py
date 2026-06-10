"""Data loading, cleaning, and team-match row construction.

The raw file is the martj42 international-results dataset. This module:

* loads and type-cleans it,
* normalizes country names that drift across eras / sources,
* splits off the Qatar 2022 group stage as a quarantined test set,
* exposes the training window with a hard leakage freeze, and
* reshapes matches into long-format team-match rows (one match -> two rows,
  one per team's goals scored), which is the unit the Poisson GLM consumes.

Zero data leakage is enforced here in code, not by convention: see
``FREEZE_DATE`` and ``assert_no_leakage``.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# --------------------------------------------------------------------------- #
# Project paths
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RAW_RESULTS = DATA / "raw" / "results.csv"
PROCESSED = DATA / "processed"
TEST_FIXTURES = DATA / "test" / "qatar2022_group_stage.csv"

# --------------------------------------------------------------------------- #
# Hard freeze: the model may only ever see matches on or before this date.
# --------------------------------------------------------------------------- #
FREEZE_DATE = pd.Timestamp("2022-11-19")

# Elo burn-in start, and the date from which ratings are trusted as features.
ELO_BURN_IN_START = pd.Timestamp("1993-01-01")
FEATURE_START = pd.Timestamp("2000-01-01")

# Qatar 2022 group stage window (the test set).
TEST_START = pd.Timestamp("2022-11-20")
TEST_END = pd.Timestamp("2022-12-02")

# --------------------------------------------------------------------------- #
# Country-name normalization
# --------------------------------------------------------------------------- #
# The dataset is mostly internally consistent, but a few names drift across
# eras and differ from external sources (eloratings.net, 538). We map historical
# / alternate names onto a single canonical label so a team's Elo carries
# forward through renames. Pre-1993 entities (West Germany, USSR, ...) are
# included for completeness even though the burn-in starts in 1993.
COUNTRY_NORMALIZATION: dict[str, str] = {
    # Germany lineage
    "West Germany": "Germany",
    "East Germany": "Germany DR",  # kept distinct; merged team is "Germany"
    # Korea
    "Korea Republic": "South Korea",
    "Korea DPR": "North Korea",
    # Ireland
    "Republic of Ireland": "Ireland",
    "Eire": "Ireland",
    # Czech lineage (Czechoslovakia dissolved 1993; treat Czech Republic as heir)
    "Czechoslovakia": "Czech Republic",
    "Czechia": "Czech Republic",
    # Yugoslavia -> Serbia and Montenegro -> Serbia lineage
    "Yugoslavia": "Serbia",
    "Serbia and Montenegro": "Serbia",
    "FR Yugoslavia": "Serbia",
    # Misc renames
    "Zaire": "DR Congo",
    "Congo DR": "DR Congo",
    "Cape Verde Islands": "Cape Verde",
    "Brunei Darussalam": "Brunei",
    "Macedonia": "North Macedonia",
    "FYR Macedonia": "North Macedonia",
    "Swaziland": "Eswatini",
    "Türkiye": "Turkey",
    "Curacao": "Curaçao",
    "St Kitts and Nevis": "Saint Kitts and Nevis",
    "St Lucia": "Saint Lucia",
    "St Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "USA": "United States",
    "Chinese Taipei": "Taiwan",
    "China PR": "China",
}


def normalize_team(name: str) -> str:
    """Map a raw team name onto its canonical label."""
    return COUNTRY_NORMALIZATION.get(name, name)


# --------------------------------------------------------------------------- #
# Loading & cleaning
# --------------------------------------------------------------------------- #
def load_raw(path: Path | str = RAW_RESULTS) -> pd.DataFrame:
    """Load and clean the raw results file.

    Returns played matches only (non-null integer scores), with parsed dates,
    a boolean ``neutral`` flag, and normalized team names. Sorted by date.
    """
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop scheduled-but-unplayed fixtures (upstream includes future rows).
    df = df.dropna(subset=["date", "home_score", "away_score"]).copy()

    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)

    # Normalize the neutral flag to a real bool (CSV stores TRUE/FALSE strings).
    if df["neutral"].dtype == object:
        df["neutral"] = (
            df["neutral"].astype(str).str.strip().str.upper().map({"TRUE": True, "FALSE": False})
        )
    df["neutral"] = df["neutral"].astype(bool)

    df["home_team"] = df["home_team"].map(normalize_team)
    df["away_team"] = df["away_team"].map(normalize_team)

    df = df.sort_values("date", kind="mergesort").reset_index(drop=True)
    return df


# --------------------------------------------------------------------------- #
# Test-set quarantine
# --------------------------------------------------------------------------- #
def extract_test_set(df: pd.DataFrame) -> pd.DataFrame:
    """Pull the 48 Qatar 2022 group-stage matches (fixtures + actual results)."""
    mask = (
        (df["date"] >= TEST_START)
        & (df["date"] <= TEST_END)
        & (df["tournament"] == "FIFA World Cup")
    )
    test = df.loc[mask].sort_values("date", kind="mergesort").reset_index(drop=True)
    return test


def training_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Matches available for training: everything on or before the freeze date."""
    return df.loc[df["date"] <= FREEZE_DATE].reset_index(drop=True)


def assert_no_leakage(df: pd.DataFrame) -> None:
    """Guard: training data must contain nothing after the freeze date."""
    latest = df["date"].max()
    if latest > FREEZE_DATE:
        raise AssertionError(
            f"Leakage detected: training data contains {latest:%Y-%m-%d}, "
            f"after freeze {FREEZE_DATE:%Y-%m-%d}."
        )


# --------------------------------------------------------------------------- #
# Long-format team-match rows
# --------------------------------------------------------------------------- #
def build_team_match_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Reshape matches into one row per team per match.

    Each match becomes two rows. ``is_home`` is 1 only for the listed home team
    on a non-neutral pitch; on neutral ground neither side gets home advantage.
    A stable ``match_id`` links the two rows of a match.
    """
    df = df.reset_index(drop=True).copy()
    df["match_id"] = df.index

    home = pd.DataFrame(
        {
            "match_id": df["match_id"],
            "date": df["date"],
            "team": df["home_team"],
            "opponent": df["away_team"],
            "goals_for": df["home_score"],
            "goals_against": df["away_score"],
            "is_home": (~df["neutral"]).astype(int),
            "neutral": df["neutral"],
            "tournament": df["tournament"],
            "side": "home",
        }
    )
    away = pd.DataFrame(
        {
            "match_id": df["match_id"],
            "date": df["date"],
            "team": df["away_team"],
            "opponent": df["home_team"],
            "goals_for": df["away_score"],
            "goals_against": df["home_score"],
            "is_home": 0,  # away team never gets the home term
            "neutral": df["neutral"],
            "tournament": df["tournament"],
            "side": "away",
        }
    )

    rows = pd.concat([home, away], ignore_index=True)
    rows = rows.sort_values(["date", "match_id", "side"], kind="mergesort").reset_index(
        drop=True
    )
    return rows
