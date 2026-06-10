#!/usr/bin/env bash
# End-to-end pipeline: raw CSV -> data + Elo -> fitted model -> backtest report.
# One command, no manual steps (PRD acceptance criterion 1).
# Usage: ./scripts/run_all.sh [tournament_key]   (default: qatar2022)
set -euo pipefail

cd "$(dirname "$0")/.."
T="${1:-qatar2022}"

echo "==> [1/3] Build data + Elo history ($T)"
python scripts/01_build_data.py "$T"

echo
echo "==> [2/3] Fit model (xi tuning + Dixon-Coles rho + sign gate + eyeball gate)"
python scripts/02_fit_model.py "$T"

echo
echo "==> [3/3] Run backtest + generate report"
python scripts/03_run_backtest.py "$T"

echo
echo "Done. See reports/${T}_backtest.md"
