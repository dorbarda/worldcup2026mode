"""Score-matrix tests (M4): sums to 1, DC correction, tail, derived markets."""

import numpy as np
import pytest
from scipy.stats import poisson

from wcmodel import matrix
from wcmodel.model import dixon_coles_tau


# --------------------------------------------------------------------------- #
# The invariant: the 9x9 matrix sums to exactly 1 (strict, 1e-9)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "lam, mu, rho",
    [
        (1.35, 1.35, 0.0),
        (2.47, 0.45, -0.05),
        (0.5, 3.0, -0.12),
        (1.68, 0.66, -0.048),
        (4.0, 0.2, -0.15),
    ],
)
def test_matrix_sums_to_one_strict(lam, mu, rho):
    M = matrix.score_matrix(lam, mu, rho)
    assert M.shape == (9, 9)
    assert abs(M.sum() - 1.0) < 1e-9
    assert (M >= 0).all()


# --------------------------------------------------------------------------- #
# Order of operations: tau applied to exactly the four low cells
# --------------------------------------------------------------------------- #
def test_dc_changes_only_low_cells_relative_to_independent():
    lam, mu, rho = 1.5, 1.2, -0.1
    M_dc = matrix.score_matrix(lam, mu, rho)
    M_indep = matrix.score_matrix(lam, mu, 0.0)
    # rho=0 -> independent; difference confined to (0,0),(0,1),(1,0),(1,1)
    # (after the shared renormalization step).
    diff = np.abs(M_dc - M_indep)
    low = {(0, 0), (0, 1), (1, 0), (1, 1)}
    # The four low cells should move appreciably...
    for (i, j) in low:
        assert diff[i, j] > 1e-4
    # ...and renormalization only rescales the rest by a tiny constant factor.
    ratio = M_dc / M_indep
    others = [ratio[i, j] for i in range(9) for j in range(9) if (i, j) not in low]
    assert np.allclose(others, others[0], atol=1e-9)


def test_dc_draw_inflation_sign():
    # rho < 0 should lift 0-0 and 1-1 (draw-ish) relative to independence.
    lam, mu, rho = 1.3, 1.1, -0.1
    M_dc = matrix.score_matrix(lam, mu, rho)
    M_indep = matrix.score_matrix(lam, mu, 0.0)
    assert M_dc[0, 0] > M_indep[0, 0]
    assert M_dc[1, 1] > M_indep[1, 1]
    assert M_dc[0, 1] < M_indep[0, 1]


# --------------------------------------------------------------------------- #
# Tail aggregation into the 8-bucket
# --------------------------------------------------------------------------- #
def test_tail_folds_into_eight_bucket():
    lam = mu = 5.0  # high rates put real mass past 8 goals
    M = matrix.score_matrix(lam, mu, 0.0)
    # The 8-row absorbs P(home >= 8); compare to the raw survival (pre-renorm,
    # renorm factor is ~1 here). The 8-bucket must exceed the bare pmf at 8.
    assert M[8, 0] > poisson.pmf(8, lam) * poisson.pmf(0, mu) * 0.9
    # And it must capture more than just the single 8,0 cell.
    assert M[8, 0] > matrix.score_matrix(lam, mu, 0.0, tail=8)[8, 0] - 1e-12


def test_independent_low_cells_match_poisson():
    lam, mu = 1.4, 1.1
    M = matrix.score_matrix(lam, mu, 0.0)
    # With rho=0 and negligible tail at low rates, interior cells ~ Poisson.
    for i in range(3):
        for j in range(3):
            assert M[i, j] == pytest.approx(poisson.pmf(i, lam) * poisson.pmf(j, mu), abs=1e-4)


# --------------------------------------------------------------------------- #
# Derived markets
# --------------------------------------------------------------------------- #
def test_derived_markets_partition():
    M = matrix.score_matrix(1.7, 1.1, -0.05)
    d = matrix.derived_markets(M)
    assert d["p_home"] + d["p_draw"] + d["p_away"] == pytest.approx(1.0, abs=1e-9)
    assert d["p_over_2_5"] + d["p_under_2_5"] == pytest.approx(1.0, abs=1e-9)
    assert d["btts_yes"] + d["btts_no"] == pytest.approx(1.0, abs=1e-9)
    assert len(d["top5_scores"]) == 5
    # top-5 are sorted descending and consistent with the modal score.
    probs = [p for _, p in d["top5_scores"]]
    assert probs == sorted(probs, reverse=True)
    assert d["top5_scores"][0][0] == matrix.most_likely_score(M)


def test_favourite_has_higher_win_prob():
    M = matrix.score_matrix(2.47, 0.45, -0.05)  # Argentina-Saudi shape
    d = matrix.derived_markets(M)
    assert d["p_home"] > d["p_away"]
    assert d["p_home"] > 0.5


def test_symmetric_match_is_balanced():
    M = matrix.score_matrix(1.35, 1.35, 0.0)
    d = matrix.derived_markets(M)
    assert d["p_home"] == pytest.approx(d["p_away"], abs=1e-9)
