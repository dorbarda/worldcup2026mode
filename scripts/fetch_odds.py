#!/usr/bin/env python3
"""Fetch bookmaker odds from The Odds API into data/external/wc2026_odds.csv.

Uses https://the-odds-api.com (free tier ~500 req/month; one call/day is plenty)
— a clean, legal, structured feed, far more reliable than scraping a bookmaker.

Set the API key as an env var (a GitHub secret in CI):

    export ODDS_API_KEY=xxxxxxxx
    python scripts/fetch_odds.py

**Fail-soft by design:** no key, a network error, or an empty response leaves the
existing odds CSV untouched and exits 0, so the daily page build never breaks.
For each fixture it writes the **median** decimal price across books (a stable
market consensus). Team names are mapped onto the pipeline's canonical labels.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import data  # noqa: E402
from wcmodel.odds import canon_team  # noqa: E402

ODDS_CSV = data.DATA / "external" / "wc2026_odds.csv"
API_KEY = os.environ.get("ODDS_API_KEY", "")
SPORT = os.environ.get("ODDS_API_SPORT", "soccer_fifa_world_cup")
API_URL = (
    "https://api.the-odds-api.com/v4/sports/{sport}/odds/"
    "?apiKey={key}&regions=us,uk,eu&markets=h2h&oddsFormat=decimal"
)

# The Odds API team names that differ from our canonical labels (post normalize_team).
API_TEAM_ALIASES = {
    "USA": "United States",
    "Korea Republic": "South Korea",
    "Korea DPR": "North Korea",
    "Czechia": "Czech Republic",
    "Turkiye": "Turkey",
    "Cabo Verde": "Cape Verde",
    "DR Congo": "DR Congo",
    "Ivory Coast": "Ivory Coast",
}


def _canon(name: str) -> str:
    # Apply known API aliases, then the shared canonicaliser (folds '&'/'and'
    # and country-name normalization) so written names match the fixtures.
    return canon_team(API_TEAM_ALIASES.get(name, name))


def parse_odds_api(events: list[dict]) -> list[dict]:
    """Turn The Odds API h2h events into odds rows (median decimal across books).

    Each event: {home_team, away_team, bookmakers:[{markets:[{key:'h2h',
    outcomes:[{name, price}]}]}]}. Soccer h2h outcomes are home, away, and 'Draw'.
    """
    rows = []
    for ev in events:
        home, away = _canon(ev.get("home_team", "")), _canon(ev.get("away_team", ""))
        prices = {"home": [], "draw": [], "away": []}
        for bk in ev.get("bookmakers", []):
            for mk in bk.get("markets", []):
                if mk.get("key") != "h2h":
                    continue
                for oc in mk.get("outcomes", []):
                    nm, price = _canon(oc.get("name", "")), oc.get("price")
                    if price is None:
                        continue
                    if nm == home:
                        prices["home"].append(price)
                    elif nm == away:
                        prices["away"].append(price)
                    elif oc.get("name", "").lower() == "draw":
                        prices["draw"].append(price)
        if prices["home"] and prices["draw"] and prices["away"]:
            rows.append({
                "home_team": home, "away_team": away,
                "odds_home": round(float(np.median(prices["home"])), 3),
                "odds_draw": round(float(np.median(prices["draw"])), 3),
                "odds_away": round(float(np.median(prices["away"])), 3),
            })
    return rows


def merge_into_csv(rows: list[dict]) -> int:
    """Upsert parsed odds rows into the CSV (by home/away). Returns rows written."""
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
    if not API_KEY:
        print("fetch_odds: no ODDS_API_KEY set — keeping the existing odds CSV.")
        return
    url = API_URL.format(sport=SPORT, key=API_KEY)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "wc2026/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            remaining = resp.headers.get("x-requests-remaining")
            events = json.loads(resp.read().decode("utf-8"))
        rows = parse_odds_api(events)
        n = merge_into_csv(rows)
        print(f"fetch_odds: updated {n} fixture(s) from The Odds API "
              f"(sport={SPORT}, requests remaining={remaining}).")
    except Exception as e:  # fail-soft: never break the daily job
        print(f"fetch_odds: fetch/parse failed ({type(e).__name__}: {e}); "
              f"keeping existing odds CSV.")


if __name__ == "__main__":
    main()
