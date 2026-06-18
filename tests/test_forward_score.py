"""Tests for forward exact-score scoring (the primary-goal scorer)."""

import numpy as np
import pandas as pd

from wcmodel import backtest as bt


def test_parse_scorelines():
    assert bt.parse_scorelines("1-0 (15%); 1-1 (13%); 0-0 (12%)") == [(1, 0), (1, 1), (0, 0)]
    assert bt.parse_scorelines("2-1 (9%)") == [(2, 1)]
    assert bt.parse_scorelines("") == []


def _row(date, h, a, lam, mu, p, top_score, top3, mkt, score):
    return {
        "date": date, "home_team": h, "away_team": a,
        "lambda_home": lam, "lambda_away": mu,
        "p_home": p[0], "p_draw": p[1], "p_away": p[2],
        "top_score": top_score, "top1_p": 0.15, "top3": top3,
        "mkt_home": mkt[0], "mkt_draw": mkt[1], "mkt_away": mkt[2],
        "home_score": score[0], "away_score": score[1],
        "outcome_idx": bt.outcome_index(score[0], score[1]),
    }


def _sample_log():
    return pd.DataFrame([
        # exact hit (pick 1-0, result 1-0), home win predicted -> directional hit
        _row("2026-06-11", "A", "B", 1.5, 0.8, (0.6, 0.25, 0.15),
             "1-0", "1-0 (15%); 1-1 (13%); 0-0 (12%)", (0.55, 0.27, 0.18), (1, 0)),
        # miss modal but result 1-1 is in top-3; actual draw -> directional miss
        _row("2026-06-11", "C", "D", 1.4, 1.0, (0.5, 0.3, 0.2),
             "1-0", "1-0 (14%); 1-1 (13%); 0-0 (12%)", (0.48, 0.30, 0.22), (1, 1)),
        # result 0-2 not in top-3; away win predicted -> directional hit
        _row("2026-06-12", "E", "F", 1.9, 0.5, (0.2, 0.25, 0.55),
             "2-0", "2-0 (16%); 1-0 (15%); 3-0 (11%)", (0.25, 0.25, 0.50), (0, 2)),
    ])


def test_score_forward_log_counts():
    s = bt.score_forward_log(_sample_log(), rho=-0.05)
    assert s["n"] == 3
    assert s["exact"] == 1          # only A-B
    assert s["top3"] == 2           # A-B and C-D
    assert s["within1"] == 2        # A-B (1-0) and C-D (1-0 vs 1-1)
    assert s["dir"] == 2            # A-B home, E-F away
    assert s["goals_actual"] == 1 + 2 + 2
    assert abs(s["xg"] - (2.3 + 2.4 + 2.4)) < 1e-9
    assert s["n_mkt"] == 3
    assert s["logloss"] > 0


def test_score_forward_log_empty():
    cols = _sample_log().columns
    empty = pd.DataFrame(columns=cols)
    s = bt.score_forward_log(empty, rho=-0.05)
    assert s["n"] == 0
