#!/usr/bin/env python3
"""Fetch bookmaker odds into data/external/wc2026_odds.csv (fail-soft).

The daily job calls this before rebuilding the page. It is **fail-soft by
design**: any error (network, geo-block, changed page layout) leaves the
existing manual odds CSV untouched and exits 0, so the page never breaks.

Scraping a live bookmaker is brittle and often against ToS, and the exact page
structure can't be validated from here — so this ships as a *scaffold*:

* point ``ODDS_SOURCE_URL`` at a page you can parse,
* implement ``parse_odds_page(html)`` to return rows of
  ``{home_team, away_team, odds_home, odds_draw, odds_away}`` (any odds format —
  ``wcmodel.odds.parse_odds`` accepts fractional / decimal / US moneyline),
* normalize team names with ``wcmodel.data.normalize_team``.

Until a source is wired up, it no-ops and the manually-maintained CSV is used.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data  # noqa: E402

ODDS_CSV = data.DATA / "external" / "wc2026_odds.csv"
SOURCE_URL = os.environ.get("ODDS_SOURCE_URL", "")


def parse_odds_page(html: str) -> list[dict]:
    """Parse a bookmaker page into odds rows. Site-specific — fill this in.

    Must return dicts with keys: home_team, away_team, odds_home, odds_draw,
    odds_away (team names normalized). Returning [] means 'nothing parsed'.
    """
    raise NotImplementedError(
        "No parser implemented. Set ODDS_SOURCE_URL and implement parse_odds_page()."
    )


def merge_into_csv(rows: list[dict]) -> int:
    """Upsert parsed odds rows into the CSV (by home/away). Returns rows changed."""
    if not rows:
        return 0
    new = pd.DataFrame(rows)
    cur = pd.read_csv(ODDS_CSV) if ODDS_CSV.exists() else pd.DataFrame(columns=new.columns)
    merged = pd.concat([cur, new]).drop_duplicates(
        subset=["home_team", "away_team"], keep="last"
    )
    ODDS_CSV.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(ODDS_CSV, index=False)
    return len(new)


def main() -> None:
    if not SOURCE_URL:
        print("fetch_odds: no ODDS_SOURCE_URL configured — keeping manual odds CSV.")
        return
    try:
        import urllib.request
        req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        rows = parse_odds_page(html)
        n = merge_into_csv(rows)
        print(f"fetch_odds: updated {n} fixture(s) from {SOURCE_URL}.")
    except Exception as e:  # fail-soft: never break the daily job
        print(f"fetch_odds: fetch/parse failed ({type(e).__name__}: {e}); "
              f"keeping existing odds CSV.")


if __name__ == "__main__":
    main()
