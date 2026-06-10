#!/usr/bin/env bash
# End-to-end pipeline: raw CSV -> data + Elo -> fitted model -> backtest report.
# One command, no manual steps (PRD acceptance criterion 1).
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> [1/3] Build data + Elo history"
python scripts/01_build_data.py

echo
echo "==> [2/3] Fit model (xi tuning + Dixon-Coles rho + sign gate + eyeball gate)"
python scripts/02_fit_model.py

echo
echo "==> [3/3] Run Qatar 2022 backtest + generate report"
python scripts/03_run_backtest.py

echo
echo "Done. See reports/qatar2022_backtest.md"
