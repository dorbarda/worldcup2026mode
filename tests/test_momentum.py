"""Mechanics tests for the experimental Elo momentum/form layer."""

import numpy as np
import pandas as pd
import pytest

from wcmodel import elo


def test_momentum_weight_excludes_friendlies():
    assert elo.momentum_weight("Friendly") == 0.0
    assert elo.momentum_weight("FIFA World Cup qualification") == 0.6
    assert elo.momentum_weight("FIFA World Cup") == 1.0
    assert elo.momentum_weight("UEFA Euro") == 1.0
    assert elo.momentum_weight("Some Minor Cup") == 0.3


def _elo_long(rows):
    return pd.DataFrame(rows)


def test_recent_competitive_win_gives_positive_momentum():
    el = _elo_long([
        {"date": pd.Timestamp("2026-05-01"), "team": "A",
         "team_elo_pre": 1500, "team_elo_post": 1512, "tournament": "FIFA World Cup qualification"},
    ])
    m = elo.momentum(el, as_of=pd.Timestamp("2026-06-01"), alpha=0.5)
    assert m["A"] > 0


def test_friendly_form_is_ignored():
    el = _elo_long([
        {"date": pd.Timestamp("2026-05-01"), "team": "A",
         "team_elo_pre": 1500, "team_elo_post": 1520, "tournament": "Friendly"},
    ])
    m = elo.momentum(el, as_of=pd.Timestamp("2026-06-01"), alpha=0.5)
    assert m.get("A", 0.0) == pytest.approx(0.0)


def test_alpha_zero_disables_and_cap_clamps():
    el = _elo_long([
        {"date": pd.Timestamp("2026-05-25"), "team": "A",
         "team_elo_pre": 1500, "team_elo_post": 1700, "tournament": "FIFA World Cup"},
    ])
    assert elo.momentum(el, pd.Timestamp("2026-06-01"), alpha=0.0).get("A", 0) == 0.0
    capped = elo.momentum(el, pd.Timestamp("2026-06-01"), alpha=5.0, cap=40.0)
    assert capped["A"] == pytest.approx(40.0)  # huge raw form clamped to the cap


def test_recency_decay_old_form_counts_less():
    recent = _elo_long([{"date": pd.Timestamp("2026-05-25"), "team": "A",
                         "team_elo_pre": 1500, "team_elo_post": 1510, "tournament": "FIFA World Cup"}])
    old = _elo_long([{"date": pd.Timestamp("2024-05-25"), "team": "A",
                      "team_elo_pre": 1500, "team_elo_post": 1510, "tournament": "FIFA World Cup"}])
    as_of = pd.Timestamp("2026-06-01")
    assert elo.momentum(recent, as_of)["A"] > elo.momentum(old, as_of)["A"]


def test_effective_ratings_adds_bonus():
    el = _elo_long([
        {"date": pd.Timestamp("2026-05-01"), "team": "A",
         "team_elo_pre": 1500, "team_elo_post": 1512, "tournament": "FIFA World Cup"},
        {"date": pd.Timestamp("2026-05-01"), "team": "B",
         "team_elo_pre": 1500, "team_elo_post": 1488, "tournament": "Friendly"},
    ])
    eff = elo.effective_ratings(el, pd.Timestamp("2026-06-01"))
    base = elo.latest_ratings(el, pd.Timestamp("2026-06-01"))
    assert eff["A"] > base["A"]          # competitive form lifts A
    assert eff["B"] == pytest.approx(base["B"])  # B's friendly form ignored
