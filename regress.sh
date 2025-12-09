#!/usr/bin/env bash
# ./util/job_launching/run_simulations.py -B rodinia_2.0-ft -C QV100-SASS -T ./hw_run/traces/device-0/12.1/ -N regtest-2025-10-30-1538

# 多个改动可以一起写在 --extra_sim_params 的同一对引号里，用空格分隔。例如：' -gpgpu_unified_l1d_size 64 -gpgpu_gmem_skip_L1D 1 '
cd $ACCELSIM_ROOT/..
echo "$PWD=$PWD"

# 单条用例模式帮助：
#   ./regress.sh single help            # 显示帮助
#   ./regress.sh single list            # 列出常见 rodinia 基准名称
#   ./regress.sh single <bench> [tag] [--extra_sim_params ' ...']
# 示例：
#   ./regress.sh single backprop-rodinia-2.0-ft
#   ./regress.sh single bfs-rodinia-2.0-ft my-bfs '--extra_sim_params -gpgpu_unified_l1d_size 64'
# 环境变量方式：
#   SINGLE_BENCH=backprop-rodinia-2.0-ft VARIANT_TAG=my-single ./regress.sh
# 说明：
# - 复用 run_simulations.py 及作业模板，stdout/stderr 自动进入 .o/.e 文件
# - 新增 --only_benchmark 过滤，不再跑整个 suite
# - 常见 rodinia 基准：backprop-rodinia-2.0-ft bfs-rodinia-2.0-ft hotspot-rodinia-2.0-ft heartwall-rodinia-2.0-ft kmeans-rodinia-2.0-ft lud-rodinia-2.0-ft nw-rodinia-2.0-ft nn-rodinia-2.0-ft pathfinder-rodinia-2.0-ft srad_v2-rodinia-2.0-ft streamcluster-rodinia-2.0-ft

if [ "$1" = "single" ]; then
  if [ "$2" = "help" ] || [ "$2" = "--help" ]; then
    cat <<'EOF'
Usage: ./regress.sh single <benchmark-name> [variant_tag] [--config-file /path/to/gpgpusim.config] [--extra_sim_params ' ...']
Examples:
  ./regress.sh single backprop-rodinia-2.0-ft
  ./regress.sh single bfs-rodinia-2.0-ft my-bfs '--extra_sim_params -gpgpu_unified_l1d_size 64'
  ./regress.sh single backprop-rodinia-2.0-ft mytag --config-file /abs/path/custom_gpgpusim.config
Environment form:
  SINGLE_BENCH=backprop-rodinia-2.0-ft VARIANT_TAG=my-single ./regress.sh
  # or with custom config file
  SINGLE_BENCH=backprop-rodinia-2.0-ft VARIANT_TAG=my-single CUSTOM_GPGPUSIM_CONFIG=/abs/path/custom_gpgpusim.config ./regress.sh
List benchmarks:
  ./regress.sh single list
Rodinia benchmarks:
  backprop-rodinia-2.0-ft
  bfs-rodinia-2.0-ft
  hotspot-rodinia-2.0-ft
  heartwall-rodinia-2.0-ft
  kmeans-rodinia-2.0-ft
  lud-rodinia-2.0-ft
  nw-rodinia-2.0-ft
  nn-rodinia-2.0-ft
  pathfinder-rodinia-2.0-ft
  srad_v2-rodinia-2.0-ft
  streamcluster-rodinia-2.0-ft
EOF
    exit 0
  fi
  if [ "$2" = "list" ]; then
    echo "Rodinia benchmark names:" 
    echo "backprop-rodinia-2.0-ft bfs-rodinia-2.0-ft hotspot-rodinia-2.0-ft heartwall-rodinia-2.0-ft kmeans-rodinia-2.0-ft lud-rodinia-2.0-ft nw-rodinia-2.0-ft nn-rodinia-2.0-ft pathfinder-rodinia-2.0-ft srad_v2-rodinia-2.0-ft streamcluster-rodinia-2.0-ft"
    exit 0
  fi
fi

if [ "$1" = "single" ]; then
  shift
  SINGLE_BENCH="$1"; shift || true
  if [[ $# -gt 0 && "$1" != --* ]]; then
    VARIANT_TAG="$1"
    shift || true
  else
    VARIANT_TAG="single-${SINGLE_BENCH}"
  fi

  # 解析可选参数，仅拦截 --config-file，其余原样并入 EXTRA_PARAMS
  CUSTOM_CFG_FILE="${CUSTOM_GPGPUSIM_CONFIG:-}"
  REM_ARGS=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --config-file|-g)
        shift
        CUSTOM_CFG_FILE="$1"
        ;;
      *)
        REM_ARGS+=("$1")
        ;;
    esac
    shift || true
  done
  EXTRA_PARAMS="${REM_ARGS[*]}" # 其余参数作为额外 sim params（可为空）

  # 如果指定了自定义 gpgpusim.config，则通过环境变量传递，供 run_simulations.py 追加覆盖
  if [ -n "$CUSTOM_CFG_FILE" ]; then
    if [ ! -f "$CUSTOM_CFG_FILE" ]; then
      echo "[ERROR] --config-file 指定的路径不存在: $CUSTOM_CFG_FILE"; exit 1
    fi
    export CUSTOM_GPGPUSIM_CONFIG="$CUSTOM_CFG_FILE"
    echo "[INFO] 使用自定义 gpgpusim.config (环境变量方式): $CUSTOM_CFG_FILE"
  fi
  if [ -z "$SINGLE_BENCH" ]; then
    echo "[ERROR] single 模式需要指定 benchmark 名称 (例如 backprop-rodinia-2.0-ft)"; exit 1
  fi
  echo "[INFO] 单条用例: $SINGLE_BENCH, variant_tag=$VARIANT_TAG"
  python3 util/job_launching/run_simulations.py \
    -B rodinia_2.0-ft \
    -C ${RUN_CFG:-QV100-SASS} \
    -T /home/hjs/dev/accel-sim/accel-sim-framework/hw_run/traces/device-0 \
    --only_benchmark "$SINGLE_BENCH" \
    --variant_tag "$VARIANT_TAG" \
    --extra_sim_params "$EXTRA_PARAMS" \
    -N "$VARIANT_TAG"
  exit $?
fi

if [ -n "$SINGLE_BENCH" ]; then
  VARIANT_TAG="${VARIANT_TAG:-single-${SINGLE_BENCH}}"
  echo "[INFO] 环境变量触发单条用例: $SINGLE_BENCH, variant_tag=$VARIANT_TAG"
  # 环境变量 CUSTOM_GPGPUSIM_CONFIG 支持：若提供，则把文件内容并入 EXTRA_PARAMS
  if [ -n "$CUSTOM_GPGPUSIM_CONFIG" ]; then
    if [ ! -f "$CUSTOM_GPGPUSIM_CONFIG" ]; then
      echo "[ERROR] CUSTOM_GPGPUSIM_CONFIG 不存在: $CUSTOM_GPGPUSIM_CONFIG"; exit 1
    fi
    echo "[INFO] 使用自定义 gpgpusim.config (环境变量方式): $CUSTOM_GPGPUSIM_CONFIG"
  fi
  python3 util/job_launching/run_simulations.py \
    -B rodinia_2.0-ft \
    -C ${RUN_CFG:-QV100-SASS} \
    -T /home/hjs/dev/accel-sim/accel-sim-framework/hw_run/traces/device-0 \
    --only_benchmark "$SINGLE_BENCH" \
    --variant_tag "$VARIANT_TAG" \
    --extra_sim_params "${EXTRA_PARAMS:-}" \
    -N "$VARIANT_TAG"
  exit $?
fi

############################################################
# Remove possible failed logs before regression to avoid a misleading message
# rm -f /home/hjs/dev/accel-sim/accel-sim-framework/util/job_launching/logfiles/*

# Example: Rodinia SASS regression with specialized-unit-4 added to SM7_QV100/trace.config
# ```
# python3 ./util/job_launching/run_simulations.py \
# -B rodinia_2.0-ft -C QV100-SASS \
# -T /home/hjs/dev/accel-sim/accel-sim-framework/hw_run/rodinia_2.0-ft/11.0 \
# -N rodinia-sass-regress-after-add-specialized-unit-4-2025-12-9-1032
# ```
# Verify above run:
# ./util/job_launching/monitor_func_test.py -v -N rodinia-sass-regress-after-add-specialized-unit-4-2025-12-9-1032
# ./util/job_launching/monitor_func_test.py -v -N rodinia-sass-regress-after-add-specialized-unit-4-2025-12-9-1104
############################################################

# 基线回归(base_config/baseline，无额外改动)
############################################################
# 
# Group (full Rodinia suite) mode with optional --config-file
# Usage examples:
#   ./regress.sh                         # default variant tag
#   ./regress.sh mytag                   # custom variant tag
#   ./regress.sh mytag --config-file /abs/path/custom.config
#   ./regress.sh --config-file /abs/path/custom.config --extra_sim_params '-gpgpu_unified_l1d_size 64'
# Environment alternative:
#   CUSTOM_GPGPUSIM_CONFIG=/abs/path/custom.config VARIANT_TAG=mytag ./regress.sh
############################################################
if [ -z "$SINGLE_BENCH" ] && [ "$1" != "single" ]; then
  # Parse args for group mode
  CUSTOM_CFG_FILE="${CUSTOM_GPGPUSIM_CONFIG:-}"
  VARIANT_TAG="${VARIANT_TAG:-fix-and-clean-2025-11-15-again}"
  REM_ARGS=()
  FIRST_NONFLAG_SEEN=0
  while [[ $# -gt 0 ]]; do
    case "$1" in
      help|--help)
        cat <<'EOF'
Group mode usage:
  ./regress.sh [variant_tag] [--config-file /path/to/gpgpusim.config] [--extra_sim_params ' ...']
Examples:
  ./regress.sh
  ./regress.sh mytag
  ./regress.sh mytag --config-file /abs/path/custom.config
  ./regress.sh --config-file /abs/path/custom.config --extra_sim_params '-gpgpu_unified_l1d_size 64'
Environment:
  VARIANT_TAG=mytag CUSTOM_GPGPUSIM_CONFIG=/abs/path/custom.config ./regress.sh
EOF
        exit 0
        ;;
      --config-file|-g)
        shift
        CUSTOM_CFG_FILE="$1"
        ;;
      --extra_sim_params)
        # preserve flag and following quoted block as-is
        REM_ARGS+=("$1")
        shift
        [ -n "$1" ] && REM_ARGS+=("$1") || true
        ;;
      --*)
        REM_ARGS+=("$1")
        ;;
      *)
        if [ $FIRST_NONFLAG_SEEN -eq 0 ]; then
          VARIANT_TAG="$1"
          FIRST_NONFLAG_SEEN=1
        else
          REM_ARGS+=("$1")
        fi
        ;;
    esac
    shift || true
  done
  EXTRA_PARAMS="${REM_ARGS[*]}"
  if [ -n "$CUSTOM_CFG_FILE" ]; then
    if [ ! -f "$CUSTOM_CFG_FILE" ]; then
      echo "[ERROR] --config-file 路径不存在: $CUSTOM_CFG_FILE"; exit 1
    fi
    export CUSTOM_GPGPUSIM_CONFIG="$CUSTOM_CFG_FILE"
    echo "[INFO] Group 模式使用自定义 gpgpusim.config (环境变量方式): $CUSTOM_CFG_FILE"
  fi
  echo "[INFO] Group 回归: variant_tag=$VARIANT_TAG"
  python3 util/job_launching/run_simulations.py \
    -B rodinia_2.0-ft \
    -C ${RUN_CFG:-QV100-SASS} \
    -T /home/hjs/dev/accel-sim/accel-sim-framework/hw_run/traces/device-0 \
    --variant_tag "$VARIANT_TAG" \
    --extra_sim_params "${EXTRA_PARAMS:-}" \
    -N "$VARIANT_TAG"
fi

# # L1D 统一容量为 64KB（示例：l1d64）
# python3 util/job_launching/run_simulations.py \
#   -B rodinia_2.0-ft \
#   -C QV100-SASS \
#   -T /home/hjs/dev/accel-sim/accel-sim-framework/hw_run/traces/device-0 \
#   --variant_tag l1d64 \
#   --extra_sim_params '-gpgpu_unified_l1d_size 64' \
#   -N reg-l1d64-2025-1031

# # 跳过 L1D（显著改动：global memory 访问绕过 L1D）
# python3 util/job_launching/run_simulations.py \
#   -B rodinia_2.0-ft \
#   -C QV100-SASS \
#   -T /home/hjs/dev/accel-sim/accel-sim-framework/hw_run/traces/device-0 \
#   --variant_tag skipL1D \
#   --extra_sim_params ' -gpgpu_unified_l1d_size 64 -gpgpu_gmem_skip_L1D 1' \
#   -N reg-skipL1D-2025-1031
