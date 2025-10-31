#!/usr/bin/env bash
set -euo pipefail

# Runs only the Rodinia benchmarks that succeeded in the last regression.
# Update the RUN_DIRS list if the passing set changes.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.."
RUN_DIRS=(
  "${ROOT_DIR}/hw_run/traces/device-0/12.1/backprop-rodinia-2.0-ft/4096___data_result_4096_txt"
  "${ROOT_DIR}/hw_run/traces/device-0/12.1/nn-rodinia-2.0-ft/__data_filelist_4_3_30_90___data_filelist_4_3_30_90_result_txt"
  "${ROOT_DIR}/hw_run/traces/device-0/12.1/pathfinder-rodinia-2.0-ft/1000_20_5___data_result_1000_20_5_txt"
)

for dir in "${RUN_DIRS[@]}"; do
  echo "Running PASS workload in ${dir}"
  (cd "${dir}" && bash run.sh)
  echo
  echo "Completed ${dir}"
  echo "------------------------------"
  echo
done
