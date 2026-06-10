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
