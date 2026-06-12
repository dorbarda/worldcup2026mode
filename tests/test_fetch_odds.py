"""The Odds API parsing + CSV upsert (fetch_odds.py)."""

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def _load():
    spec = importlib.util.spec_from_file_location("fetch_odds", SCRIPTS / "fetch_odds.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SAMPLE = [{
    "home_team": "USA", "away_team": "Paraguay",
    "bookmakers": [
        {"markets": [{"key": "h2h", "outcomes": [
            {"name": "USA", "price": 2.00}, {"name": "Draw", "price": 3.40},
            {"name": "Paraguay", "price": 3.80}]}]},
        {"markets": [{"key": "h2h", "outcomes": [
            {"name": "USA", "price": 2.10}, {"name": "Draw", "price": 3.30},
            {"name": "Paraguay", "price": 4.00}]}]},
    ],
}]


def test_parse_maps_names_and_takes_median():
    fo = _load()
    rows = fo.parse_odds_api(SAMPLE)
    assert len(rows) == 1
    r = rows[0]
    assert r["home_team"] == "United States"  # USA alias -> canonical
    assert r["away_team"] == "Paraguay"
    assert r["odds_home"] == pytest.approx(2.05)  # median of 2.00, 2.10
    assert r["odds_away"] == pytest.approx(3.90)


def test_parse_skips_incomplete_events():
    fo = _load()
    bad = [{"home_team": "Spain", "away_team": "Cape Verde",
            "bookmakers": [{"markets": [{"key": "h2h", "outcomes": [
                {"name": "Spain", "price": 1.1}]}]}]}]  # missing draw/away
    assert fo.parse_odds_api(bad) == []


def test_merge_upserts_by_fixture(tmp_path, monkeypatch):
    fo = _load()
    csv = tmp_path / "odds.csv"
    csv.write_text("home_team,away_team,odds_home,odds_draw,odds_away\n"
                   "United States,Paraguay,1.9,3.5,4.2\n")
    monkeypatch.setattr(fo, "ODDS_CSV", csv)
    n = fo.merge_into_csv([{"home_team": "United States", "away_team": "Paraguay",
                            "odds_home": 2.05, "odds_draw": 3.35, "odds_away": 3.9}])
    out = pd.read_csv(csv)
    assert n == 1 and len(out) == 1  # upsert, not duplicate
    assert out.iloc[0]["odds_home"] == pytest.approx(2.05)  # last wins
