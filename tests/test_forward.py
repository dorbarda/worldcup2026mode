"""Forward-prediction tests: as-of routing and predict_match orientation."""

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

from wcmodel import data

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def _load_predict_match():
    spec = importlib.util.spec_from_file_location("predict_match", SCRIPTS / "predict_match.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- #
# As-of artifact routing keeps the frozen backtest dir isolated
# --------------------------------------------------------------------------- #
def test_asof_proc_dir_qatar_is_canonical():
    assert data.asof_proc_dir(data.QATAR2022.freeze) == data.PROCESSED


def test_asof_proc_dir_other_date_is_namespaced():
    d = data.asof_proc_dir(pd.Timestamp("2026-06-10"))
    assert d == data.PROCESSED / "asof_2026-06-10"
    assert d != data.PROCESSED  # never collides with the frozen artifacts


# --------------------------------------------------------------------------- #
# predict_match orientation: --home gives that side home advantage
# --------------------------------------------------------------------------- #
def test_resolve_orientation_home_and_neutral():
    pm = _load_predict_match()
    assert pm._resolve_orientation("Mexico", "South Africa", "Mexico") == (
        "Mexico", "South Africa", False)
    assert pm._resolve_orientation("Mexico", "South Africa", "South Africa") == (
        "South Africa", "Mexico", False)
    # No --home -> neutral venue, team1 on the row axis.
    assert pm._resolve_orientation("Brazil", "Argentina", None) == (
        "Brazil", "Argentina", True)


def test_resolve_orientation_rejects_bad_home():
    pm = _load_predict_match()
    with pytest.raises(SystemExit):
        pm._resolve_orientation("Mexico", "South Africa", "Brazil")


# --------------------------------------------------------------------------- #
# predict_fixtures: "each team's next match" selection drives the update loop
# --------------------------------------------------------------------------- #
def _load_predict_fixtures():
    spec = importlib.util.spec_from_file_location(
        "predict_fixtures", SCRIPTS / "predict_fixtures.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _group_schedule():
    # One group of 4 (A,B,C,D), three matchdays, dates in order.
    rounds = [
        ("2026-06-11", "A", "B"), ("2026-06-11", "C", "D"),   # matchday 1
        ("2026-06-15", "A", "C"), ("2026-06-15", "B", "D"),   # matchday 2
        ("2026-06-19", "A", "D"), ("2026-06-19", "B", "C"),   # matchday 3
    ]
    return pd.DataFrame(
        [{"date": pd.Timestamp(d), "home_team": h, "away_team": a, "neutral": True}
         for d, h, a in rounds]
    )


def test_next_round_is_each_teams_next_match():
    pf = _load_predict_fixtures()
    sched = _group_schedule()
    nr = pf.next_round(sched)
    # Matchday 1: two matches covering all four teams exactly once.
    assert len(nr) == 2
    teams = set(nr.home_team) | set(nr.away_team)
    assert teams == {"A", "B", "C", "D"}
    assert (nr["date"] == pd.Timestamp("2026-06-11")).all()


def test_next_round_advances_when_earlier_matches_drop_off():
    pf = _load_predict_fixtures()
    sched = _group_schedule()
    # Simulate matchday 1 played (removed from the unplayed pool).
    remaining = sched[sched["date"] > pd.Timestamp("2026-06-11")].reset_index(drop=True)
    nr = pf.next_round(remaining)
    assert len(nr) == 2
    assert (nr["date"] == pd.Timestamp("2026-06-15")).all()
