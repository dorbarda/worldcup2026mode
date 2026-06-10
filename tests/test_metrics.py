"""Metric tests (M5): RPS, log loss, Brier on hand-computed examples."""

import numpy as np
import pytest

from wcmodel import backtest as bt
from wcmodel import matrix as mx


# --------------------------------------------------------------------------- #
# Outcome indexing
# --------------------------------------------------------------------------- #
def test_outcome_index():
    assert bt.outcome_index(2, 0) == 0  # home win
    assert bt.outcome_index(1, 1) == 1  # draw
    assert bt.outcome_index(0, 2) == 2  # away win


# --------------------------------------------------------------------------- #
# RPS
# --------------------------------------------------------------------------- #
def test_rps_perfect_is_zero():
    assert bt.rps([1, 0, 0], 0) == pytest.approx(0.0)
    assert bt.rps([0, 1, 0], 1) == pytest.approx(0.0)


def test_rps_worst_case():
    # Certain home, but away happened: cum diffs (1-0, 1-0)=1,1 -> 0.5*(1+1)=1.
    assert bt.rps([1, 0, 0], 2) == pytest.approx(1.0)


def test_rps_hand_computed():
    # p=[0.5,0.3,0.2], home wins.
    # cum p=[0.5,0.8]; cum o=[1,1]; sq=(0.25+0.04); /2 = 0.145
    assert bt.rps([0.5, 0.3, 0.2], 0) == pytest.approx(0.145)


def test_rps_ordinal_penalty():
    # Predicting away-heavy is punished more when home wins than draw-heavy.
    p = [0.2, 0.2, 0.6]
    assert bt.rps(p, 0) > bt.rps(p, 1) > bt.rps(p, 2)


# --------------------------------------------------------------------------- #
# Brier
# --------------------------------------------------------------------------- #
def test_brier_perfect_and_worst():
    assert bt.brier_1x2([1, 0, 0], 0) == pytest.approx(0.0)
    assert bt.brier_1x2([1, 0, 0], 2) == pytest.approx(2.0)


def test_brier_hand_computed():
    # p=[0.5,0.3,0.2], home: (0.5-1)^2 + 0.3^2 + 0.2^2 = 0.25+0.09+0.04 = 0.38
    assert bt.brier_1x2([0.5, 0.3, 0.2], 0) == pytest.approx(0.38)


# --------------------------------------------------------------------------- #
# Exact-score log loss
# --------------------------------------------------------------------------- #
def test_exact_log_loss_matches_cell():
    M = mx.score_matrix(1.5, 1.2, -0.05)
    ll = bt.exact_log_loss(M, 1, 0)
    assert ll == pytest.approx(-np.log(M[1, 0]))


def test_exact_log_loss_caps_tail():
    M = mx.score_matrix(1.5, 1.2, -0.05)
    # A 10-3 result caps into the (8, 3) bucket.
    assert bt.exact_log_loss(M, 10, 3) == pytest.approx(-np.log(M[8, 3]))


def test_exact_log_loss_lower_for_likelier_score():
    M = mx.score_matrix(2.4, 0.5, -0.05)  # strong favourite
    # A 2-0 (likely) should score a lower loss than 0-3 (unlikely).
    assert bt.exact_log_loss(M, 2, 0) < bt.exact_log_loss(M, 0, 3)


# --------------------------------------------------------------------------- #
# Aggregation + calibration
# --------------------------------------------------------------------------- #
def test_score_1x2_frame():
    probs = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
    outcomes = np.array([0, 1, 2])
    s = bt.score_1x2_frame(probs, outcomes)
    assert s["rps"] == pytest.approx(0.0)
    assert s["brier"] == pytest.approx(0.0)
    assert s["n"] == 3


def test_calibration_perfect_predictions():
    # Deterministic correct predictions land near the 0 and 1 bins on-diagonal.
    probs = np.array([[1, 0, 0]] * 5 + [[0, 1, 0]] * 5, dtype=float)
    outcomes = np.array([0] * 5 + [1] * 5)
    cal = bt.calibration_points(probs, outcomes)
    for _, r in cal.iterrows():
        assert r["realized"] == pytest.approx(r["predicted"], abs=1e-9)
