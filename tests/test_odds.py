"""Odds parsing/de-vig and the forward-log result backfill (market comparison)."""

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from wcmodel import odds

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


# --------------------------------------------------------------------------- #
# Parsing & de-vig
# --------------------------------------------------------------------------- #
def test_parse_odds_fractional_and_decimal():
    assert odds.parse_odds("4/9") == pytest.approx(1 + 4 / 9)
    assert odds.parse_odds("1/1") == pytest.approx(2.0)
    assert odds.parse_odds("1.44") == pytest.approx(1.44)
    assert odds.parse_odds(2.5) == pytest.approx(2.5)


def test_implied_probs_sum_to_one_and_devig():
    p = odds.implied_probs("4/9", "15/4", "17/2")
    assert p.sum() == pytest.approx(1.0)
    # Matches the hand figure: ~0.69 / 0.21 / 0.10.
    assert p[0] == pytest.approx(0.687, abs=0.01)
    assert p[2] == pytest.approx(0.104, abs=0.01)


def test_parse_odds_american_moneyline():
    assert odds.parse_odds("+150") == pytest.approx(2.5)
    assert odds.parse_odds("-200") == pytest.approx(1.5)
    assert odds.parse_odds("+100") == pytest.approx(2.0)
    assert odds.parse_odds("-3000") == pytest.approx(1 + 100 / 3000)
    assert odds.parse_odds(260) == pytest.approx(3.6)  # unsigned magnitude >= 100


def test_implied_probs_american_favourite():
    p = odds.implied_probs("-160", "+285", "+475")  # Brazil-Morocco shape
    assert p.sum() == pytest.approx(1.0)
    assert p[0] > p[1] > p[2]  # home favoured


def test_overround_positive_for_vigged_book():
    assert odds.overround("4/9", "15/4", "17/2") > 0
    assert odds.overround("-3000", "+1500", "+2800") > 0  # American too


def test_implied_probs_ordering_favours_shorter_odds():
    p = odds.implied_probs("11/100", "12/1", "28/1")  # huge favourite
    assert p[0] > 0.85 and p[0] > p[1] > p[2]


# --------------------------------------------------------------------------- #
# load_market aligns to fixtures; None when absent
# --------------------------------------------------------------------------- #
def test_load_market_alignment(tmp_path):
    csv = tmp_path / "odds.csv"
    csv.write_text(
        "home_team,away_team,odds_home,odds_draw,odds_away\n"
        "Mexico,South Africa,4/9,15/4,17/2\n"
    )
    fixtures = pd.DataFrame({"home_team": ["Mexico"], "away_team": ["South Africa"]})
    m = odds.load_market(fixtures, csv)
    assert m.shape == (1, 3)
    assert m[0].sum() == pytest.approx(1.0)


def test_load_market_missing_file_is_none():
    assert odds.load_market(pd.DataFrame({"home_team": [], "away_team": []}),
                            "/no/such/file.csv") is None


# --------------------------------------------------------------------------- #
# Forward-log result backfill must key on DATE (no historical-friendly bleed)
# --------------------------------------------------------------------------- #
def _load_predict_fixtures():
    spec = importlib.util.spec_from_file_location(
        "predict_fixtures", SCRIPTS / "predict_fixtures.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _prediction_row():
    return pd.DataFrame([{
        "date": pd.Timestamp("2026-06-13"), "home_team": "Brazil", "away_team": "Morocco",
        "p_home": 0.44, "p_draw": 0.30, "p_away": 0.26,
        "mkt_home": 0.58, "mkt_draw": 0.24, "mkt_away": 0.18,
    }])


def test_forward_log_ignores_past_friendly_same_teams(tmp_path, monkeypatch):
    pf = _load_predict_fixtures()
    monkeypatch.setattr(pf, "FORWARD_LOG", tmp_path / "log.csv")
    # A historical Brazil-Morocco friendly on a different date must NOT backfill.
    played = pd.DataFrame([{
        "date": pd.Timestamp("2023-03-25"), "home_team": "Brazil",
        "away_team": "Morocco", "home_score": 1, "away_score": 2}])
    pf._update_forward_log(_prediction_row(), played)
    log = pd.read_csv(tmp_path / "log.csv")
    assert pd.isna(log.loc[0, "outcome_idx"])  # result stays blank


def test_forward_log_backfills_on_matching_date(tmp_path, monkeypatch):
    pf = _load_predict_fixtures()
    monkeypatch.setattr(pf, "FORWARD_LOG", tmp_path / "log.csv")
    pf._update_forward_log(_prediction_row(), pd.DataFrame(columns=["date", "home_team", "away_team", "home_score", "away_score"]))
    # Now the actual WC fixture is played on its scheduled date.
    played = pd.DataFrame([{
        "date": pd.Timestamp("2026-06-13"), "home_team": "Brazil",
        "away_team": "Morocco", "home_score": 2, "away_score": 1}])
    pf._update_forward_log(_prediction_row(), played)
    log = pd.read_csv(tmp_path / "log.csv")
    assert len(log) == 1  # not duplicated on the second call
    assert log.loc[0, "outcome_idx"] == 0  # home win backfilled
