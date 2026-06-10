"""Betting-odds ingestion: parse, de-vig, and align to fixtures.

Used as a **comparison / edge layer**, not as a model input — the Dixon-Coles
model stays independent. De-vigged market probabilities are shown alongside the
model's and logged forward so the market baseline (B2) can finally be scored
against real results during the tournament.

Odds may be fractional ("4/9") or decimal ("1.44"); both map to a decimal odd,
and implied probabilities are the normalized inverse-odds (vig removed).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .data import DATA


def parse_odds(value) -> float:
    """Return decimal odds (> 1) from a fractional string, decimal string, or number."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    s = str(value).strip()
    if "/" in s:
        num, den = s.split("/")
        return 1.0 + float(num) / float(den)
    return float(s)


def implied_probs(home, draw, away) -> np.ndarray:
    """De-vigged [P(home), P(draw), P(away)] from three odds (any format)."""
    dec = np.array([parse_odds(home), parse_odds(draw), parse_odds(away)], dtype=float)
    raw = 1.0 / dec
    return raw / raw.sum()


def overround(home, draw, away) -> float:
    """Bookmaker margin (vig): sum of inverse-odds minus 1."""
    dec = np.array([parse_odds(home), parse_odds(draw), parse_odds(away)], dtype=float)
    return float((1.0 / dec).sum() - 1.0)


def load_market(fixtures: pd.DataFrame, path: Path | str | None = None):
    """De-vigged market probs aligned to ``fixtures`` rows, or None if unavailable.

    CSV columns: ``home_team, away_team, odds_home, odds_draw, odds_away`` (team
    names normalized to match the pipeline). Returns an (n, 3) array; rows whose
    fixture has no odds are filled with NaN (so partial coverage is fine).
    """
    path = Path(path) if path is not None else (DATA / "external" / "wc2026_odds.csv")
    if not Path(path).exists():
        return None
    odds = pd.read_csv(path)
    odds["home_team"] = odds["home_team"].astype(str)
    odds["away_team"] = odds["away_team"].astype(str)
    merged = fixtures.merge(odds, on=["home_team", "away_team"], how="left")

    out = np.full((len(merged), 3), np.nan)
    for i, r in enumerate(merged.itertuples(index=False)):
        if pd.notna(getattr(r, "odds_home", np.nan)):
            out[i] = implied_probs(r.odds_home, r.odds_draw, r.odds_away)
    if np.isnan(out).all():
        return None
    return out
