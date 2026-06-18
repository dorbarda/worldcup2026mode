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
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from wcmodel import backtest as bt, data, matrix as mx, odds  # noqa: E402
from wcmodel.forward import current_ratings, load_schedule, next_round, refresh_snapshot  # noqa: E402,F401
from wcmodel.model import FittedModel  # noqa: E402

FORWARD_LOG = data.DATA / "external" / "wc2026_forward_log.csv"


# Forward-log schema. The prediction block (lambdas, 1X2, exact-score picks,
# market) is refreshed each run *until the match is played*; once a result lands
# the row is locked, so the scored forecast is the freshest pre-kickoff one.
LOG_COLS = ["date", "home_team", "away_team", "model_version",
            "lambda_home", "lambda_away", "p_home", "p_draw", "p_away",
            "top_score", "top1_p", "top3",
            "mkt_home", "mkt_draw", "mkt_away",
            "home_score", "away_score", "outcome_idx"]
# Columns refreshed on every run while a fixture is still unplayed.
PRED_COLS = ["model_version", "lambda_home", "lambda_away", "p_home", "p_draw", "p_away",
             "top_score", "top1_p", "top3", "mkt_home", "mkt_draw", "mkt_away"]


def _update_forward_log(out: pd.DataFrame, played: pd.DataFrame) -> None:
    """Accumulate {prediction, market, exact-score, result} per fixture, forward.

    Freshness policy ("refresh until kickoff"): a fixture's prediction block is
    re-written from the current run while the match is still unplayed, then
    **locked** the moment a result is backfilled — so the forecast we score is
    the last one published before kickoff (no stale pre-logged forecasts). The
    exact-score pick (the project's primary goal) is recorded alongside 1X2 so it
    can be scored forward, not just reconstructed from git.
    """
    log = pd.read_csv(FORWARD_LOG) if FORWARD_LOG.exists() else pd.DataFrame(columns=LOG_COLS)
    log = log.reindex(columns=LOG_COLS)  # tolerate an older, narrower schema
    pos = {(r.home_team, r.away_team, pd.to_datetime(r.date).date()): i
           for i, r in enumerate(log.itertuples())}

    def _payload(r) -> dict:
        return {"model_version": r.model_version,
                "lambda_home": r.lam_full, "lambda_away": r.mu_full,
                "p_home": r.p_home, "p_draw": r.p_draw, "p_away": r.p_away,
                "top_score": r.top_score, "top1_p": r.top1_p, "top3": r.top3,
                "mkt_home": r.mkt_home, "mkt_draw": r.mkt_draw, "mkt_away": r.mkt_away}

    for r in out.itertuples(index=False):
        key = (r.home_team, r.away_team, pd.Timestamp(r.date).date())
        if key not in pos:  # first time we predict this fixture
            row = {"date": key[2], "home_team": r.home_team, "away_team": r.away_team,
                   **_payload(r), "home_score": np.nan, "away_score": np.nan, "outcome_idx": np.nan}
            log.loc[len(log)] = row
            pos[key] = len(log) - 1
        elif pd.isna(log.at[pos[key], "home_score"]):  # unplayed -> refresh forecast
            for c, v in _payload(r).items():
                log.at[pos[key], c] = v

    # Backfill results from the snapshot for any logged fixture now played. Key on
    # (home, away, DATE) so a past friendly between the same teams can't masquerade
    # as the WC fixture result. A backfilled result locks the row from here on.
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
        scored = done[done["mkt_home"].notna()]
        msg = f"\nForward scoring over {len(done)} completed match(es):  model RPS {m_rps:.4f}"
        if len(scored):
            os_ = scored["outcome_idx"].astype(int).to_numpy()
            k_rps = np.mean([bt.rps(p, os_[i]) for i, p in
                             enumerate(scored[["mkt_home", "mkt_draw", "mkt_away"]].to_numpy())])
            ms_rps = np.mean([bt.rps(p, os_[i]) for i, p in
                              enumerate(scored[["p_home", "p_draw", "p_away"]].to_numpy())])
            msg += (f"  |  vs market over {len(scored)}: model {ms_rps:.4f} / market {k_rps:.4f}"
                    f" ({'model ahead' if ms_rps < k_rps else 'market ahead'})")
        # Exact-score scoreboard — the primary goal.
        exact = int((done["top_score"] == done["home_score"].astype("Int64").astype(str) + "-"
                     + done["away_score"].astype("Int64").astype(str)).sum())
        msg += f"\nExact-score hits (top pick == result): {exact}/{len(done)}"
        print(msg)


def main() -> None:
    ap = argparse.ArgumentParser(description="2026 group-stage predictions from current Elo.")
    ap.add_argument("--all", action="store_true",
                    help="predict all remaining group games (default: each team's next match)")
    ap.add_argument("--refresh", action="store_true", help="re-download the results snapshot first")
    ap.add_argument("--model", default=str(data.forward_model_path()))
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
    model_version = "v2" if model.goal_scale != 1.0 else "v1"
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
        (ms_h, ms_a), top1_p = d["top5_scores"][0]
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
            # full-precision helpers for the forward log (dropped before the report CSV)
            "model_version": model_version, "lam_full": lam, "mu_full": mu, "top1_p": float(top1_p),
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

    # Result backfill runs unconditionally — it doesn't require market odds.
    _update_forward_log(out, played)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.drop(columns=["lam_full", "mu_full", "top1_p"], errors="ignore").to_csv(args.out, index=False)
    print(f"\nWrote {Path(args.out).relative_to(data.ROOT)}"
          + (f" + heatmaps in reports/figures/wc2026/" if args.plot else ""))
    print("Update loop: once these are played, re-run with --refresh for the next matchday.")


if __name__ == "__main__":
    main()
