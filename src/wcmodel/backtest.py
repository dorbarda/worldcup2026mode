"""Backtest protocol for Qatar 2022 (M5): freeze, predict, score.

Predictions for all 48 group matches are generated **as of the freeze**
(2022-11-19) from a single ratings snapshot -- Elo is *not* updated between
rounds, matching a pre-tournament forecast and side-stepping round-3
dead-rubber contamination debates.

Metrics (three layers, PRD 5.2):

* exact-score hit rate -- modal predicted score == actual (a vanity metric),
* probabilistic: RPS on 1X2 (primary), log loss on the exact-score cell,
  Brier on 1X2 (secondary),
* calibration: 1X2 probabilities bucketed and compared to realized frequency.

Outcome ordering for 1X2 is ordinal: index 0 = home win, 1 = draw, 2 = away win.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from . import matrix as mx
from .data import FREEZE_DATE
from .model import FittedModel

# Round boundaries within the group stage (for the dead-rubber split).
ROUND12_END = pd.Timestamp("2022-11-28")  # rounds 1-2 are 20-28 Nov; round 3 after


# --------------------------------------------------------------------------- #
# Outcome helpers
# --------------------------------------------------------------------------- #
def outcome_index(home_goals: int, away_goals: int) -> int:
    """0 = home win, 1 = draw, 2 = away win."""
    if home_goals > away_goals:
        return 0
    if home_goals == away_goals:
        return 1
    return 2


def onehot3(idx: int) -> np.ndarray:
    o = np.zeros(3)
    o[idx] = 1.0
    return o


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #
def rps(probs: np.ndarray, outcome_idx: int) -> float:
    """Ranked Probability Score for one match (ordinal 1X2). Lower is better."""
    p = np.asarray(probs, dtype=float)
    o = onehot3(outcome_idx)
    cp = np.cumsum(p)
    co = np.cumsum(o)
    # r = 3 outcomes -> average over the first r-1 = 2 cumulative steps.
    return float(np.sum((cp[:-1] - co[:-1]) ** 2) / (len(p) - 1))


def brier_1x2(probs: np.ndarray, outcome_idx: int) -> float:
    """Multiclass Brier score for one match: sum of squared errors over 3 classes."""
    p = np.asarray(probs, dtype=float)
    o = onehot3(outcome_idx)
    return float(np.sum((p - o) ** 2))


def exact_log_loss(M: np.ndarray, home_goals: int, away_goals: int) -> float:
    """Negative log probability the matrix assigned to the actual exact score.

    Goals are capped into the tail bucket so every result has a cell.
    """
    n = M.shape[0] - 1
    x = min(int(home_goals), n)
    y = min(int(away_goals), n)
    p = max(float(M[x, y]), 1e-15)
    return -float(np.log(p))


# --------------------------------------------------------------------------- #
# Prediction generation (the model)
# --------------------------------------------------------------------------- #
def predict_fixture(
    model: FittedModel,
    ratings: pd.Series,
    home: str,
    away: str,
    neutral: bool,
) -> dict:
    """Full prediction for one fixture: lambdas, matrix, 1X2 and derived markets."""
    lam, mu = model.fixture_lambdas(ratings, home, away, neutral=neutral)
    M = mx.score_matrix(lam, mu, model.rho)
    d = mx.derived_markets(M)
    return {
        "lambda_home": lam,
        "lambda_away": mu,
        "matrix": M,
        "p_home": d["p_home"],
        "p_draw": d["p_draw"],
        "p_away": d["p_away"],
        "p_over_2_5": d["p_over_2_5"],
        "btts_yes": d["btts_yes"],
        "top5_scores": d["top5_scores"],
        "modal_score": mx.most_likely_score(M),
    }


def generate_predictions(
    model: FittedModel,
    test_fixtures: pd.DataFrame,
    ratings: pd.Series,
) -> pd.DataFrame:
    """Predict every test fixture from the frozen ratings snapshot.

    ``test_fixtures`` carries the actual results, but those are only *read back*
    for scoring -- predictions depend solely on the pre-freeze ratings.
    """
    rows = []
    for r in test_fixtures.itertuples(index=False):
        pred = predict_fixture(model, ratings, r.home_team, r.away_team, bool(r.neutral))
        probs = np.array([pred["p_home"], pred["p_draw"], pred["p_away"]])
        oidx = outcome_index(r.home_score, r.away_score)
        rows.append(
            {
                "date": r.date,
                "home_team": r.home_team,
                "away_team": r.away_team,
                "neutral": bool(r.neutral),
                "lambda_home": pred["lambda_home"],
                "lambda_away": pred["lambda_away"],
                "p_home": pred["p_home"],
                "p_draw": pred["p_draw"],
                "p_away": pred["p_away"],
                "p_over_2_5": pred["p_over_2_5"],
                "btts_yes": pred["btts_yes"],
                "modal_home": pred["modal_score"][0],
                "modal_away": pred["modal_score"][1],
                "top3": pred["top5_scores"][:3],
                "home_score": int(r.home_score),
                "away_score": int(r.away_score),
                "outcome_idx": oidx,
                "rps": rps(probs, oidx),
                "brier": brier_1x2(probs, oidx),
                "log_loss": exact_log_loss(pred["matrix"], r.home_score, r.away_score),
                "hit": (pred["modal_score"] == (int(r.home_score), int(r.away_score))),
            }
        )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# Aggregate scoring (works for any 1X2 prediction source)
# --------------------------------------------------------------------------- #
def score_1x2_frame(probs: np.ndarray, outcomes: np.ndarray) -> dict:
    """Mean RPS and Brier for a stack of 1X2 predictions vs realized outcomes."""
    rps_vals = [rps(probs[i], int(outcomes[i])) for i in range(len(outcomes))]
    brier_vals = [brier_1x2(probs[i], int(outcomes[i])) for i in range(len(outcomes))]
    return {
        "rps": float(np.mean(rps_vals)),
        "brier": float(np.mean(brier_vals)),
        "n": int(len(outcomes)),
    }


# --------------------------------------------------------------------------- #
# Calibration
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# Forward exact-score scoring (the primary goal, measured live)
# --------------------------------------------------------------------------- #
_SCORELINE = re.compile(r"(\d+)\s*-\s*(\d+)")


def parse_scorelines(text: str) -> list[tuple[int, int]]:
    """Extract ``[(h, a), ...]`` from a "1-0 (15%); 1-1 (13%)" top-3 string."""
    return [(int(h), int(a)) for h, a in _SCORELINE.findall(str(text))]


def score_forward_log(log: pd.DataFrame, rho: float) -> dict:
    """Score completed forward-log rows on the exact-score goal (and 1X2).

    The headline exact / top-3 hits use the **published** picks (``top_score`` /
    ``top3``) so we grade exactly what we forecast. Deeper diagnostics (top-5,
    exact-score log loss, goal bias) rebuild the matrix from the stored lambdas.
    """
    done = log[log["outcome_idx"].notna()].copy()
    recs = []
    for r in done.itertuples(index=False):
        hs, as_ = int(r.home_score), int(r.away_score)
        actual = (hs, as_)
        top3 = parse_scorelines(r.top3)
        # rebuilt matrix for the deeper metrics (uses stored lambdas)
        if pd.notna(r.lambda_home) and pd.notna(r.lambda_away):
            M = mx.score_matrix(float(r.lambda_home), float(r.lambda_away), rho)
            d = mx.derived_markets(M)
            top5 = [s for s, _ in d["top5_scores"]]
            in_top5 = actual in top5
            logloss = exact_log_loss(M, hs, as_)
            p_actual = float(M[min(hs, M.shape[0] - 1), min(as_, M.shape[1] - 1)])
            xg = float(r.lambda_home) + float(r.lambda_away)
        else:
            in_top5, logloss, p_actual, xg = np.nan, np.nan, np.nan, np.nan
        probs = np.array([r.p_home, r.p_draw, r.p_away], dtype=float)
        oidx = int(r.outcome_idx)
        recs.append({
            "date": r.date, "home_team": r.home_team, "away_team": r.away_team,
            "actual": f"{hs}-{as_}", "top_score": r.top_score,
            "exact_hit": str(r.top_score) == f"{hs}-{as_}",
            "in_top3": actual in top3, "in_top5": in_top5,
            "within1": abs((top3[0][0] if top3 else -9) - hs) <= 1
                       and abs((top3[0][1] if top3 else -9) - as_) <= 1,
            "dir_hit": int(np.argmax(probs)) == oidx,
            "logloss": logloss, "p_actual": p_actual,
            "total_goals": hs + as_, "xg": xg,
            "rps": rps(probs, oidx),
            "mkt_rps": rps(np.array([r.mkt_home, r.mkt_draw, r.mkt_away], dtype=float), oidx)
                       if pd.notna(r.mkt_home) else np.nan,
        })
    per = pd.DataFrame(recs)
    if per.empty:
        return {"n": 0, "per_match": per}
    mkt = per.dropna(subset=["mkt_rps"])
    return {
        "n": len(per),
        "exact": int(per["exact_hit"].sum()),
        "top3": int(per["in_top3"].sum()),
        "top5": int(per["in_top5"].sum(skipna=True)),
        "within1": int(per["within1"].sum()),
        "dir": int(per["dir_hit"].sum()),
        "rps": float(per["rps"].mean()),
        "mkt_rps": float(mkt["mkt_rps"].mean()) if len(mkt) else float("nan"),
        "mkt_rps_model": float(mkt["rps"].mean()) if len(mkt) else float("nan"),
        "n_mkt": int(len(mkt)),
        "logloss": float(per["logloss"].mean(skipna=True)),
        "goals_actual": int(per["total_goals"].sum()),
        "xg": float(per["xg"].sum(skipna=True)),
        "per_match": per,
    }


def calibration_points(
    probs: np.ndarray, outcomes: np.ndarray, n_bins: int = 10
) -> pd.DataFrame:
    """Flatten all 1X2 probabilities into (predicted, realized) and bin them.

    Each match contributes 3 points (one per outcome). Returns per-bin mean
    predicted probability vs realized hit frequency.
    """
    flat_p = probs.reshape(-1)
    flat_o = np.concatenate([onehot3(int(o)) for o in outcomes])
    bins = np.linspace(0, 1, n_bins + 1)
    idx = np.clip(np.digitize(flat_p, bins) - 1, 0, n_bins - 1)
    out = []
    for b in range(n_bins):
        m = idx == b
        if m.sum() == 0:
            continue
        out.append(
            {
                "bin": b,
                "mid": (bins[b] + bins[b + 1]) / 2,
                "predicted": float(flat_p[m].mean()),
                "realized": float(flat_o[m].mean()),
                "count": int(m.sum()),
            }
        )
    return pd.DataFrame(out)
