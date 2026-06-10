#!/usr/bin/env python3
"""Batch group-stage predictions for the 2026 World Cup, from current Elo.

Designed for an "update as we go" loop:

1. Each run computes Elo from **all played matches** in the snapshot (current).
2. By default it predicts **each team's next unplayed group match** — right now
   that's every team's opener (24 matches). Once those results are added to the
   snapshot and Elo updates, the same command rolls forward to the next matchday.
3. ``--refresh`` re-downloads the martj42 results snapshot first, so newly played
   matches flow into Elo automatically.

The model *coefficients* come from the frozen, backtest-validated 2022-11-19 fit;
the *ratings* are current. Knockouts are out of scope (no ET/penalties layer).

Examples:
    python scripts/predict_fixtures.py                 # each team's next match
    python scripts/predict_fixtures.py --refresh        # pull latest results first
    python scripts/predict_fixtures.py --all            # all remaining group games
    python scripts/predict_fixtures.py --plot           # also save heatmaps
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import backtest as bt, data, elo, matrix as mx, odds  # noqa: E402
from wcmodel.model import FittedModel  # noqa: E402

FORWARD_LOG = data.DATA / "external" / "wc2026_forward_log.csv"

RESULTS_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
WC_TOURNAMENT = "FIFA World Cup"


def refresh_snapshot() -> None:
    """Re-download the results snapshot so new results feed current Elo."""
    print(f"Refreshing snapshot from {RESULTS_URL} ...")
    urllib.request.urlretrieve(RESULTS_URL, data.RAW_RESULTS)
    print(f"  wrote {data.RAW_RESULTS.relative_to(data.ROOT)}")


def load_schedule() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (played, upcoming_wc) frames with normalized team names."""
    raw = pd.read_csv(data.RAW_RESULTS)
    raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
    raw = raw.dropna(subset=["date"])
    raw["home_team"] = raw["home_team"].map(data.normalize_team)
    raw["away_team"] = raw["away_team"].map(data.normalize_team)
    if raw["neutral"].dtype == object:
        raw["neutral"] = raw["neutral"].astype(str).str.upper().map(
            {"TRUE": True, "FALSE": False}
        )
    raw["neutral"] = raw["neutral"].astype(bool)

    played = raw.dropna(subset=["home_score", "away_score"]).copy()
    upcoming = raw[
        (raw["tournament"] == WC_TOURNAMENT) & (raw["home_score"].isna())
    ].sort_values("date", kind="mergesort").reset_index(drop=True)
    return played, upcoming


def next_round(upcoming: pd.DataFrame) -> pd.DataFrame:
    """Each team's next unplayed match: greedy over date order.

    A match is included iff neither team has already been claimed by an earlier
    match. On a full group stage this returns exactly the next matchday.
    """
    seen: set[str] = set()
    keep = []
    for fx in upcoming.itertuples(index=False):
        if fx.home_team in seen or fx.away_team in seen:
            continue
        keep.append(fx)
        seen.update([fx.home_team, fx.away_team])
    return pd.DataFrame(keep)


def current_ratings(played: pd.DataFrame) -> tuple[pd.Series, pd.Timestamp]:
    elo_long = elo.compute_elo(played.sort_values("date", kind="mergesort"))
    as_of = played["date"].max()
    return elo.latest_ratings(elo_long, as_of + pd.Timedelta(days=1)), as_of


def _update_forward_log(out: pd.DataFrame, played: pd.DataFrame) -> None:
    """Accumulate {prediction, market, result} per fixture for forward B2 scoring.

    Predictions are logged **once** (the pre-match forecast is never overwritten,
    even if a later run's Elo would change it). Results are backfilled from the
    snapshot as matches get played. Once results exist, prints model-vs-market
    RPS — the market baseline (B2) finally scored, honestly, going forward.
    """
    cols = ["date", "home_team", "away_team", "p_home", "p_draw", "p_away",
            "mkt_home", "mkt_draw", "mkt_away", "home_score", "away_score", "outcome_idx"]
    log = pd.read_csv(FORWARD_LOG) if FORWARD_LOG.exists() else pd.DataFrame(columns=cols)
    keyed = {(r.home_team, r.away_team) for r in log.itertuples(index=False)}

    new = out[out["mkt_home"].notna()].copy()
    for r in new.itertuples(index=False):
        if (r.home_team, r.away_team) in keyed:
            continue  # keep the first (pre-match) forecast
        log.loc[len(log)] = {
            "date": pd.Timestamp(r.date).date(), "home_team": r.home_team, "away_team": r.away_team,
            "p_home": r.p_home, "p_draw": r.p_draw, "p_away": r.p_away,
            "mkt_home": r.mkt_home, "mkt_draw": r.mkt_draw, "mkt_away": r.mkt_away,
            "home_score": np.nan, "away_score": np.nan, "outcome_idx": np.nan,
        }

    # Backfill results from the snapshot for any logged fixture now played.
    # Key on (home, away, DATE) so a past friendly between the same teams can't
    # masquerade as the WC fixture result.
    res = {(r.home_team, r.away_team, pd.Timestamp(r.date).date()): (r.home_score, r.away_score)
           for r in played.itertuples(index=False)}
    for idx, row in log.iterrows():
        key = (row["home_team"], row["away_team"], pd.to_datetime(row["date"]).date())
        if pd.isna(row["home_score"]) and key in res:
            hs, as_ = res[key]
            log.at[idx, "home_score"] = hs
            log.at[idx, "away_score"] = as_
            log.at[idx, "outcome_idx"] = bt.outcome_index(hs, as_)

    FORWARD_LOG.parent.mkdir(parents=True, exist_ok=True)
    log.to_csv(FORWARD_LOG, index=False)

    done = log[log["outcome_idx"].notna()]
    if len(done):
        o = done["outcome_idx"].astype(int).to_numpy()
        m_rps = np.mean([bt.rps(p, o[i]) for i, p in
                         enumerate(done[["p_home", "p_draw", "p_away"]].to_numpy())])
        k_rps = np.mean([bt.rps(p, o[i]) for i, p in
                         enumerate(done[["mkt_home", "mkt_draw", "mkt_away"]].to_numpy())])
        print(f"\nForward B2 scoring over {len(done)} completed match(es):  "
              f"model RPS {m_rps:.4f}  |  market RPS {k_rps:.4f}  "
              f"({'model ahead' if m_rps < k_rps else 'market ahead'})")


def main() -> None:
    ap = argparse.ArgumentParser(description="2026 group-stage predictions from current Elo.")
    ap.add_argument("--all", action="store_true",
                    help="predict all remaining group games (default: each team's next match)")
    ap.add_argument("--refresh", action="store_true", help="re-download the results snapshot first")
    ap.add_argument("--model", default=str(data.PROCESSED / "model.json"))
    ap.add_argument("--out", default=str(data.ROOT / "reports" / "wc2026_predictions.csv"))
    ap.add_argument("--plot", action="store_true", help="save a heatmap PNG per fixture")
    ap.add_argument("--odds", default=str(data.DATA / "external" / "wc2026_odds.csv"),
                    help="de-vigged market comparison CSV (home_team,away_team,odds_home,odds_draw,odds_away)")
    ap.add_argument("--edge", type=float, default=0.10,
                    help="flag fixtures where |model - market| on any outcome >= this (default 0.10)")
    args = ap.parse_args()

    if args.refresh:
        refresh_snapshot()

    model = FittedModel.load(args.model)
    played, upcoming = load_schedule()
    if upcoming.empty:
        raise SystemExit("No upcoming FIFA World Cup fixtures in the snapshot.")

    fixtures = upcoming if args.all else next_round(upcoming)
    snap, as_of = current_ratings(played)
    market = odds.load_market(fixtures, args.odds)  # (n,3) de-vigged or None

    label = "all remaining group games" if args.all else "each team's next match"
    print(f"\n2026 World Cup — {label}  ({len(fixtures)} fixtures)")
    print(f"Elo current as of {as_of:%Y-%m-%d}; model coeffs frozen 2022-11-19."
          + ("  Market = de-vigged odds." if market is not None else "  (no odds file)") + "\n")

    rows = []
    for i, fx in enumerate(fixtures.itertuples(index=False)):
        h, a, neutral = fx.home_team, fx.away_team, bool(fx.neutral)
        if h not in snap.index or a not in snap.index:
            continue
        lam, mu = model.fixture_lambdas(snap, h, a, neutral=neutral)
        M = mx.score_matrix(lam, mu, model.rho)
        d = mx.derived_markets(M)
        (ms_h, ms_a), _ = d["top5_scores"][0]
        mkt = market[i] if market is not None else (np.nan, np.nan, np.nan)
        edge = float(np.nanmax(np.abs(np.array([d["p_home"], d["p_draw"], d["p_away"]]) - mkt))) \
            if market is not None and not np.isnan(mkt).all() else np.nan
        rows.append({
            "date": fx.date, "home_team": h, "away_team": a,
            "venue": "neutral" if neutral else f"{h} home",
            "lambda_home": round(lam, 2), "lambda_away": round(mu, 2),
            "p_home": round(d["p_home"], 3), "p_draw": round(d["p_draw"], 3),
            "p_away": round(d["p_away"], 3), "p_over_2_5": round(d["p_over_2_5"], 3),
            "btts_yes": round(d["btts_yes"], 3),
            "mkt_home": round(mkt[0], 3), "mkt_draw": round(mkt[1], 3), "mkt_away": round(mkt[2], 3),
            "edge": round(edge, 3) if edge == edge else np.nan,
            "top_score": f"{ms_h}-{ms_a}",
            "top3": "; ".join(f"{i2}-{j2} ({p*100:.0f}%)" for (i2, j2), p in d["top5_scores"][:3]),
        })

        if args.plot:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig_dir = data.ROOT / "reports" / "figures" / "wc2026"
            fig_dir.mkdir(parents=True, exist_ok=True)
            _, ax = plt.subplots(figsize=(6.5, 6))
            mx.render_matrix(M, h, a, lam, mu, ax=ax)
            plt.tight_layout()
            plt.savefig(fig_dir / f"{fx.date:%m%d}_{h}_{a}.png".replace(" ", "_"), dpi=110)
            plt.close()

    out = pd.DataFrame(rows)
    have_mkt = market is not None
    # Pretty console table (market columns only when odds are present).
    if have_mkt:
        hdr = (f"{'Date':<7}{'Match':<33}{'V':<8}{'OUR H/D/A':<18}{'MKT H/D/A':<18}{'edge':<6}{'Top':<5}")
    else:
        hdr = f"{'Date':<7}{'Match':<35}{'Venue':<9}{'λ H/A':<12}{'H / D / A':<19}{'O2.5':<6}{'Top':<5}"
    print(hdr)
    print("-" * len(hdr))
    for r in out.itertuples(index=False):
        venue = "neutral" if r.venue == "neutral" else "host"
        match = f"{r.home_team} v {r.away_team}"[:32]
        ours = f"{r.p_home:.2f}/{r.p_draw:.2f}/{r.p_away:.2f}"
        if have_mkt:
            mk = "  —  " if r.mkt_home != r.mkt_home else f"{r.mkt_home:.2f}/{r.mkt_draw:.2f}/{r.mkt_away:.2f}"
            flag = "  " if (r.edge != r.edge) else ("<<" if r.edge >= args.edge else "  ")
            print(f"{r.date:%b %d} {match:<33}{venue:<8}{ours:<18}{mk:<18}"
                  f"{('' if r.edge!=r.edge else f'{r.edge:.2f}'):<6}{flag}")
        else:
            print(f"{r.date:%b %d} {match:<35}{venue:<9}"
                  f"{f'{r.lambda_home}/{r.lambda_away}':<12}{ours:<19}{r.p_over_2_5:<6.2f}{r.top_score:<5}")

    # Edge summary: biggest disagreements with the market.
    if have_mkt and out["edge"].notna().any():
        big = out[out["edge"] >= args.edge].sort_values("edge", ascending=False)
        if len(big):
            print(f"\nEdges vs market (|Δ| ≥ {args.edge:.2f}) — where our model disagrees most:")
            for r in big.itertuples(index=False):
                lean = "model higher on home" if r.p_home > r.mkt_home else "model lower on home"
                print(f"  {r.home_team} v {r.away_team}: ours {r.p_home:.2f}/{r.p_draw:.2f}/{r.p_away:.2f} "
                      f"vs mkt {r.mkt_home:.2f}/{r.mkt_draw:.2f}/{r.mkt_away:.2f}  ({lean})")
        _update_forward_log(out, played)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(f"\nWrote {Path(args.out).relative_to(data.ROOT)}"
          + (f" + heatmaps in reports/figures/wc2026/" if args.plot else ""))
    print("Update loop: once these are played, re-run with --refresh for the next matchday.")


if __name__ == "__main__":
    main()
