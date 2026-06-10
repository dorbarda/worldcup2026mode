"""Leakage guard tests (M1): no post-freeze data may reach training."""

import pandas as pd
import pytest

from wcmodel import data


def test_training_frame_respects_freeze():
    raw = data.load_raw()
    train = data.training_frame(raw)
    assert train["date"].max() <= data.FREEZE_DATE


def test_assert_no_leakage_passes_on_clean_frame():
    raw = data.load_raw()
    train = data.training_frame(raw)
    data.assert_no_leakage(train)  # must not raise


def test_assert_no_leakage_raises_on_dirty_frame():
    dirty = pd.DataFrame({"date": pd.to_datetime(["2022-11-20"])})
    with pytest.raises(AssertionError):
        data.assert_no_leakage(dirty)


def test_test_set_is_48_matches_in_window():
    raw = data.load_raw()
    test = data.extract_test_set(raw)
    assert len(test) == 48
    assert test["date"].min() >= data.TEST_START
    assert test["date"].max() <= data.TEST_END
    assert (test["tournament"] == "FIFA World Cup").all()


def test_test_set_disjoint_from_training():
    raw = data.load_raw()
    train = data.training_frame(raw)
    test = data.extract_test_set(raw)
    # No test match date should appear inside the training window.
    assert train["date"].max() < test["date"].min()


def test_qatar_match_is_home_others_neutral():
    raw = data.load_raw()
    test = data.extract_test_set(raw)
    qatar = test[(test.home_team == "Qatar") | (test.away_team == "Qatar")]
    # Qatar's group matches: the one where Qatar is home must be non-neutral.
    qatar_home = test[test.home_team == "Qatar"]
    assert len(qatar_home) >= 1
    assert not qatar_home["neutral"].iloc[0]
    # Every non-Qatar-hosted match is neutral ground.
    non_qatar = test[(test.home_team != "Qatar")]
    assert non_qatar["neutral"].all()


def test_normalization_examples():
    assert data.normalize_team("Korea Republic") == "South Korea"
    assert data.normalize_team("West Germany") == "Germany"
    assert data.normalize_team("England") == "England"


def test_build_team_match_rows_shape_and_semantics():
    raw = data.load_raw().head(100)
    rows = data.build_team_match_rows(raw)
    assert len(rows) == 2 * len(raw)
    # Home team on neutral ground gets no home advantage.
    neutral_home = rows[(rows.side == "home") & (rows.neutral)]
    assert (neutral_home["is_home"] == 0).all()
    # Away rows are never home.
    assert (rows[rows.side == "away"]["is_home"] == 0).all()
    # Non-neutral home rows are home.
    nonneutral_home = rows[(rows.side == "home") & (~rows.neutral)]
    assert (nonneutral_home["is_home"] == 1).all()
