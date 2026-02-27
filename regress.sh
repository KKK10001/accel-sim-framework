#!/usr/bin/env bash
# ./util/job_launching/run_simulations.py -B rodinia_2.0-ft -C QV100-SASS -T ./hw_run/rodinia_2.0-ft/11.0/ -N regtest-2025-10-30-1538

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
  EXTRA_PARAMS=""
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
  EXTRA_ARGS=()
  if [ -n "$EXTRA_PARAMS" ]; then
    EXTRA_ARGS=(--extra_sim_params "$EXTRA_PARAMS")
  fi

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
  CMD=(
    python3 util/job_launching/run_simulations.py
    -B rodinia_2.0-ft
    -C "${RUN_CFG:-QV100-SASS}"
    -T ~/dev/accel-sim/accel-sim-framework/hw_run/rodinia_2.0-ft/11.0
    --only_benchmark "$SINGLE_BENCH"
    --variant_tag "$VARIANT_TAG"
  )
  CMD+=("${EXTRA_ARGS[@]}")
  CMD+=(-N "$VARIANT_TAG")
  "${CMD[@]}"
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
  EXTRA_ARGS=()
  if [ -n "${EXTRA_PARAMS:-}" ]; then
    EXTRA_ARGS=(--extra_sim_params "${EXTRA_PARAMS}")
  fi
  CMD=(
    python3 util/job_launching/run_simulations.py
    -B rodinia_2.0-ft
    -C "${RUN_CFG:-QV100-SASS}"
    -T ~/dev/accel-sim/accel-sim-framework/hw_run/rodinia_2.0-ft/11.0
    --only_benchmark "$SINGLE_BENCH"
    --variant_tag "$VARIANT_TAG"
  )
  CMD+=("${EXTRA_ARGS[@]}")
  CMD+=(-N "$VARIANT_TAG")
  "${CMD[@]}"
  exit $?
fi

############################################################
# Remove possible failed logs before regression to avoid a misleading message
# rm -f ~/dev/accel-sim/accel-sim-framework/util/job_launching/logfiles/*

# Example: Directly use regress.sh
# ./regress.sh $VARIANT_TAG

# Example: Passing paras one-by-one to run_simulations.py
# ```
# python3 ./util/job_launching/run_simulations.py \
# -B rodinia_2.0-ft -C QV100-SASS \
# -T ~/dev/accel-sim/accel-sim-framework/hw_run/rodinia_2.0-ft/11.0 \
# --variant_tag "$VARIANT_TAG" \
# -N "$VARIANT_TAG"
# ```
# Verify above run:
# ./util/job_launching/monitor_func_test.py -v -N rodinia-sass-regress-after-add-specialized-unit-4-2025-12-9-1417
############################################################

# 基线回归(base_config/baseline，无额外改动)
############################################################
# 
# Group (full Rodinia suite) mode with optional --config-file
# Usage examples:
#   ./regress.sh                         # default variant tag
#   ./regress.sh ${mytag} --config-file /abs/path/custom.config

# ./regress.sh xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --config-file ./perf_study/configs/l1p5_remain_line_size.config
# ./regress.sh exclude_memcpy_from_cache_timing --config-file ./perf_study/configs/l1p5_remain_line_size.config
# ./regress.sh exclude_memcpy_from_cache_timing_again --config-file ./perf_study/configs/l1p5_remain_line_size.config

# ./regress.sh reg_no_mshr_l2_dram_q_size_8 --config-file ./perf_study/configs/l1p5_mshr_max_merge_0_l2_dram_queue_size_64.config
# ok
# ./regress.sh default_memcpy_offset_check_again --config-file ./perf_study/configs/l1p5_remain_line_size.config

# 2026-1-2
# ok (Use this as baseline of Arise2)
# ./regress.sh regress_no_mshr_l2_dram_q_size_8 --config-file ./perf_study/configs/l1p5_no_mshr_l2_dram_q_size_8.config
# ok
# ./regress.sh regress_no_mshr_l2_dram_q_size_64 --config-file ./perf_study/configs/l1p5_no_mshr_l2_dram_q_size_64.config

# 2026-1-5
# ./regress.sh reg_check_if_dram_byapss_l2_directly_to_icnt_path_exists --config-file ./perf_study/configs/l1p5_subs_1x2_mshr_max_merge_4_l2_dram_q_size_2.config
# ./regress.sh reg_check_if_dram_byapss_l2_directly_to_icnt_path_exists_again --config-file ./perf_study/configs/l1p5_subs_1x2_mshr_max_merge_4_l2_dram_q_size_2.config

# Contents of /home/kuanbba/dev/accel-sim/accel-sim-framework/util/job_launching/../../sim_run_12.1/heartwall-rodinia-2.0-ft/__data_test_avi_1___data_result_1_txt/QV100-SASS/regress_subs_2x2_no_mshr_l2_dram_q_size_8/heartwall-rodinia-2.0-ft-__data_test_avi_1___data_result_1_txt.e895
# ------------------
# accel-sim.out: delayqueue.h:69: void fifo_pipeline<T>::push(T*) [with T = mem_fetch]: Assertion `m_length < m_max_len' failed.

# 2026-1-8
# ./regress.sh regress_disable_mshr__l1p5_subs_4x2_mshr_max_merge_4_l2_dram_q_size_8 --config-file ./perf_study/configs/l1p5_subs_4x2_mshr_max_merge_4_l2_dram_q_size_8.config

# ./regress.sh regress_disable_mshr__l1p5_subs_4x2_mshr_max_merge_4_l2_dram_q_size_8_again --config-file ./perf_study/configs/l1p5_subs_4x2_mshr_max_merge_4_l2_dram_q_size_8.config

# 11:59-12:05 ALL PASS
# ./regress.sh regress_disable_mshr_l1p5_correlation --config-file ./perf_study/configs/l1p5_correlation.config
# 12:07-ALL PASS
# ./regress.sh regress_disable_mshr_l2_correlation --config-file ./perf_study/configs/l1p5_correlation.config
# ./regress.sh regress_enable_mshr_l2_correlation --config-file ./perf_study/configs/l1p5_correlation.config

# 1-9 
# ok
# ./regress.sh regress_disable_mshr --config-file ./perf_study/configs/l2_corr_mshr_disable.config

# ./regress.sh regress_enable_mshr --config-file ./perf_study/configs/l2_corr_mshr_enable.config

# ok 11:51
# ./regress.sh regress_disable_mshr_use_macro_again --config-file ./perf_study/configs/l2_corr.config
# ./regress.sh regress_enable_mshr_use_macro_again --config-file ./perf_study/configs/l2_corr.config

# 15:27-:32
# ./regress.sh regress_disable_all_mshr --config-file ./perf_study/configs/l2_corr_mshr_disable.config
# :33-:36
# ./regress.sh regress_enable_all_mshr --config-file ./perf_study/configs/l2_corr_mshr_enable.config

# ./regress.sh regress_subs_2x2_no_mshr_l2_dram_q_size_8 --config-file ./perf_study/configs/l1p5_subs_2x2_no_mshr_l2_dram_q_size_8.config

# 1-12
# ./regress.sh regress_en_all_mshr_l2_mshr_ent_192_slots_4 --config-file ./perf_study/configs/l2_corr_mshr_enable.config

# ./regress.sh regress_disable_all_mshr_1_13 --config-file ./perf_study/configs/l2_corr_mshr_disable.config
# ./regress.sh regress_enable_all_mshr_1_13 --config-file ./perf_study/configs/l2_corr_mshr_enable.config

# 1-15
# ./regress.sh regress_mshr_correlated_repl --config-file ./perf_study/configs/l2_corr_mshr_enable.config
# ./regress.sh regress_mshr_correlated_repl_II --config-file ./perf_study/configs/l2_corr_mshr_enable.config
# ./regress.sh regress_mshr_correlated_repl_fixed_bug --config-file ./perf_study/configs/l2_corr_mshr_enable.config
# 14:23-:31 ok
# ./regress.sh regress_mshr_corr_repl_pass_cfg_val --config-file ./perf_study/configs/l2_corr_mshr_correlated_repl.config
# 14:32-42 ok
# ./regress.sh regress_mshr_enable_default_repl --config-file ./perf_study/configs/l2_corr_mshr_enable_default_repl.config
# 14:43
# ./regress.sh regress_disable_mshr_baseline --config-file ./perf_study/configs/l2_corr_mshr_disable.config
# 16:32 
# ./regress.sh regress_mshr_correlated_repl_3rd_time --config-file ./perf_study/configs/l2_corr_mshr_correlated_repl.config
# 16:40
# ./regress.sh regress_disable_mshr_baseline_3rd_time --config-file ./perf_study/configs/l2_corr_mshr_disable.config
# 16:53
# ./regress.sh regress_mshr_correlated_repl_4th_time_remove_mshr_m_code --config-file ./perf_study/configs/l2_corr_mshr_correlated_repl.config
# 17:03
# ./regress.sh regress_mshr_correlated_repl_5th_time_remove_mshr_m_code --config-file ./perf_study/configs/l2_corr_mshr_correlated_repl.config
# 17:23
# ./regress.sh regress_mshr_correlated_repl_modify_final_rep_result_with_mshr_m_logic --config-file ./perf_study/configs/l2_corr_mshr_correlated_repl.config
# 17:39 
# ./regress.sh regress_mshr_correlated_repl_modify_only_use_mshr_m_logic --config-file ./perf_study/configs/l2_corr_mshr_correlated_repl.config

# 1-16 SRRIP
# 11:54 one group seems hang
# ./regress.sh regress_mshr_disable_rep_srrip --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip.config
# 13:55
# 13:59 streamcluster finished
# 14:01 srad_v2 is still running
# ./regress.sh regress_mshr_disable_rep_srrip_again --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip.config
# 15:01 
# ./regress.sh regress_mshr_disable_rep_srrip_bugfix_rrpv_2_when_fill --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip.config
# 16:17
# ./regress.sh regress_mshr_disable_rep_srrip_bugfix_continue_probe_tag_onlyif_miss --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip.config
# 16:37-
# ./regress.sh regress_mshr_disable_1_16_confirm_again --config-file ./perf_study/configs/l2_corr_mshr_disable.config
# 18:52
# ./regress.sh regress_mshr_disable_rep_srrip_keep_reserve_fail_otherwise_hang --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip.config
# 19:04
# ./regress.sh regress_mshr_disable_1_16_eve_confirm_after_srrip_fix_reserve_issue --config-file ./perf_study/configs/l2_corr_mshr_disable.config
# 19:20
# ./regress.sh regress_mshr_disable_rep_srrip_inc_rrpv_for_one_set_ok --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip.config
# 1-17 
# 8:49 (IPC: -0.189%) (a little drop compared with rrpv_2_when_allocate. Confusion)
# ./regress.sh regress_mshr_disable_rep_srrip_rrpv_3_when_allocate_when_inv --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip.config
# 9:04 (IPC: -0.415%)
# ./regress.sh regress_mshr_disable_rep_srrip_rrpv_3_when_allocate_when_inv_wr_ratio_0 --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip_wr_ratio_0.config
# 13:02
# ./regress.sh regress_mshr_disable_rep_srrip_rrpv_2_bits --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip_rrpv_2bits.config
# ./regress.sh regress_mshr_disable_combined_srrip_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_rep_srrip_rrpv_2bits.config
# ./regress.sh regress_mshr_disable_dcache_srrip_other_lru_combined_srrip_lru_implement --config-file ./perf_study/configs/l2_corr_mshr_disable_dcache_srrip_other_lru.config
# ./regress.sh regress_mshr_disable_l2_srrip_other_lru_combined_srrip_lru_implement --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_other_lru.config
# ./regress.sh regress_mshr_disable_l2_combined_rep_other_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_combined_rep_other_lru.config
# ./regress.sh regress_mshr_disable_l2_srrip_rrpv_3bits_other_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_rrpv_3bits_other_lru.config

# 1-19
# ./regress.sh regress_mshr_disable --config-file ./perf_study/configs/l2_corr_mshr_disable.config
# 29.721 (-0.548%)
# ./regress.sh regress_mshr_disable_l1d_l2_srrip_other_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_l1d_l2_srrip_other_lru.config
# 29.970 (+0.285%)
# ./regress.sh regress_mshr_disable_l2_srrip_other_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_other_lru.config
# 29.970 (+0.285%)
# ./regress.sh regress_mshr_disable_l2_srrip_lru_switch_other_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_lru_switch_other_lru.config
# 29.943 (+0.197%) drops.  RRIP-FP (Frequency Policy)
# ./regress.sh regress_mshr_disable_l2_srrip_fp_other_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_fp_other_lru.config
# 29.970 (+0.285%) RRIP-HP
# ./regress.sh regress_mshr_disable_l2_srrip_hp_other_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_other_lru.config
# 29.854 (-0.103%) worse
# ./regress.sh regress_mshr_disable_l2_srrip_hp_other_lru_again --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_other_lru.config
# 29.970 (+0.285%) line->inc_rrpv() during each step of "SRRIP && force_using_lru"
# ./regress.sh regress_mshr_disable_l2_srrip_hp_other_lru_3rd --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_other_lru.config
# 29.721 (-0.548%) worse! It seems that SRRIP can only be used for L2
# ./regress.sh regress_mshr_disable_l1d_l2_srrip_hp_other_lru_3rd --config-file ./perf_study/configs/l2_corr_mshr_disable_l1d_l2_srrip_hp_other_lru.config
# 29.970 (+0.285%) no use of setting max rrpv after LRU's picking valid index
# ./regress.sh regress_mshr_disable_l2_srrip_hp_set_max_rrpv_for_lru_picked_index --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_other_lru.config
# 29.884 (+0.000%)
# ./regress.sh regress_mshr_disable_all_cache_lru.o --config-file ./perf_study/configs/l2_corr_mshr_disable_all_cache_lru.config
# 17:40
# ./regress.sh regress_mshr_disable_modify_lru_picked_index_with_srrip_update_logic --config-file ./perf_study/configs/l2_corr_mshr_disable_all_cache_lru.config
# 18:02 29.970 (+0.285%) the same as just using srrip
# ./regress.sh regress_mshr_disable_l2_srrip_hp_lru_switch_other_lru --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_lru_switch_other_lru.config
# 18:33 29.925 (+0.135%)
# ./regress.sh reg_l1d_l2_srrip_hp_lru_switch_rrpv_half_max_when_allocate --config-file ./perf_study/configs/l2_corr_mshr_disable_l1d_l2_srrip_hp_lru_switch_other_lru.config
# 29.963 (+0.264%) following should be renamed as "half_max + 1"
# ./regress.sh reg_l2_srrip_hp_lru_switch_rrpv_half_max_when_allocate --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_lru_switch_other_lru.config
# ./regress.sh reg_l2_srrip_hp_rrpv_half_max_when_allocate --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_other_lru.config
# 29.886 (+0.007%)
# ./regress.sh reg_l2_srrip_hp_rrpv_half_max_when_allocate_again --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_other_lru.config
# 29.890 (+0.019%)
# ./regress.sh reg_l2_srrip_hp_rrpv_half_max_plus_1_when_allocate --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_other_lru.config
# Compare with "reg_l2_srrip_hp_lru_switch_rrpv_half_max_when_allocate"
# 29.963 (+0.264%) !!! srrip switch to lru do help perf!!!
# ./regress.sh reg_l2_srrip_hp_lru_switch_rrpv_half_max_plus_1_when_allocate --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_lru_switch_other_lru.config
# 29.929 (+0.148%) worse. When allocate, do not set rrpv too hot
# ./regress.sh reg_l2_srrip_hp_lru_switch_rrpv_0_when_allocate --config-file ./perf_study/configs/l2_corr_mshr_disable_l2_srrip_hp_lru_switch_other_lru.config

# ./regress.sh reg_en_l2_mshr_l2_srrip_hp_lru_switch_half_max_plus_1_when_allocate --config-file ./perf_study/configs/en_l2_mshr_l2_srrip_hp_lru_switch_other_lru.config

# 1-19 20:56 34.293 (+14.751%)
# ./regress.sh reg_en_all_mshr_all_cache_lru --config-file ./perf_study/configs/en_all_mshr_all_cache_lru.config
# 21:06 34.439 (+15.242%)
# ./regress.sh reg_en_all_mshr_all_cache_mshr_corr_rep --config-file ./perf_study/configs/en_all_mshr_all_cache_mshr_corr_rep.config
# 1-20 8:41 34.397 (+15.099%) drops ---> record more info. would be better
# ./regress.sh reg_en_all_mshr__rep_pick_records_below_4_in_mshr --config-file ./perf_study/configs/en_all_mshr_all_cache_mshr_corr_rep.config
# 9:19 34.229 (+14.537%) worse
# ./regress.sh reg_en_all_mshr_pick_max_interval_in_mshr --config-file ./perf_study/configs/en_all_mshr_all_cache_mshr_corr_rep.config
# 34.435 (+15.228%) min_records win
# ./regress.sh reg_en_all_mshr_pick_min_records_in_mshr --config-file ./perf_study/configs/en_all_mshr_all_cache_mshr_corr_rep.config
# 9:39 34.435 (+15.228%) -> l2 mshr slots = 4 is already enough
# ./regress.sh reg_en_all_mshr_pick_min_records_in_mshr_l2_mshr_merge_8 --config-file ./perf_study/configs/en_all_mshr_all_cache_mshr_corr_rep_l2_mshr_merge_8.config
# 13:58 34.440 (+15.245%) best until now. l2_assoc: 16->32 saved a lot of RESERVATION_FAILS
# ./regress.sh reg_en_all_mshr_all_cache_mshr_corr_rep_l2_assoc_32 --config-file ./perf_study/configs/en_all_mshr_all_cache_mshr_corr_rep_l2_assoc_32.config
# 15:16 34.442 (+15.250%) Best! Really works!
# ./regress.sh reg_mshr_aware_rep --config-file ./perf_study/configs/en_all_mshr_all_cache_mshr_corr_rep_l2_assoc_32.config

# 17:15-:25 34.316 (+14.830%) drops. Guess: low-latency cache such as l1d should still use LRU.
# ./regress.sh reg_mshr_aware_mixed_rep_l1d_l2_prime_srrip --config-file ./perf_study/configs/mshr_aware_mixed_rep_l1d_l2_prime_srrip.config
# 17:27-:33 34.460 (+15.309%) Best! (MSHR-aware + LRU)
# ./regress.sh reg_mshr_aware_mixed_rep_l2_prime_lru --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_lru.config
# 17:35-:39 34.460 (+15.309%) Same
# ./regress.sh reg_mshr_aware_mixed_rep_l2_prime_srrip --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_srrip.config

# 1-21 8:47 regress after splitting stats of sector_misses and misses
# 29.869 (+0.000%)
# ./regress.sh reg_mshr_disable_all_cache_rep_lru --config-file ./perf_study/configs/mshr_disable_all_cache_rep_lru.config
# 34.296 (+14.822%)
# ./regress.sh reg_en_all_mshr_all_cache_lru --config-file ./perf_study/configs/en_all_mshr_all_cache_lru.config
# 34.357 (+15.029%) Apply SRRIP only to L2 would help
# ./regress.sh reg_en_all_mshr_l2_srrip --config-file ./perf_study/configs/en_all_mshr_l2_srrip.config
# 34.290 (+14.803%) drops. Increasing l2_assoc would not necessarily improve IPC
# ./regress.sh reg_en_all_mshr_l2_srrip_l2_assoc_32 --config-file ./perf_study/configs/en_all_mshr_l2_srrip_l2_assoc_32.config
# 34.281 (+14.772%) drops L2_miss_rate: 0.116 (+44.843%)  L1D_miss_rate: 0.169 (+2.598%)
# ./regress.sh reg_mshr_aware_mixed_rep_l1d_l2_prime_srrip --config-file ./perf_study/configs/mshr_aware_mixed_rep_l1d_l2_prime_srrip.config
# 34.264 (+14.717%) do not use L1 SRRIP
# ./regress.sh reg_mshr_aware_mixed_rep_l1d_l2_prime_srrip_l1d_assoc_64_l2_assoc_16 --config-file ./perf_study/configs/mshr_aware_mixed_rep_l1d_l2_prime_srrip_l1d_assoc_64_l2_assoc_16.config


# 34.442 (+15.313%)
# ./regress.sh reg_mshr_aware_mixed_rep_l2_prime_lru --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_lru.config
# 34.460 (+15.372%) Better than LRU on L2
# ./regress.sh reg_mshr_aware_mixed_rep_l2_prime_srrip --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_srrip.config
# 34.424 drops. when l2_prime_lru/_srrip with l2_assoc_32. Larger assoc would make delay on evicting of cold lines

# 1-21 Fight!!! 15:09 34.458 (+15.365%)
# ./regress.sh reg_l1d_evict_aware_lru_mshr_aware_mixed_rep_l2_prime_srrip --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_srrip.config
# 34.458 (+15.365%)
# ./regress.sh reg_l1d_evict_aware_judge_since_30_percent --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_srrip.config
# 34.458 (+15.365%)
# ./regress.sh reg_l1d_evict_aware_reverse_judge_cond_evict_ratio_larger_than_lru_picked --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_srrip.config

# ./regress.sh reg_l1d_evict_aware_judge_since_30_percent_disable_mshr_aware --config-file ./perf_study/configs/en_all_mshr_l2_srrip.config

# 1-21 16:56
# ./regress.sh reg_l1d_re_ref_interval_aware_lru --config-file ./perf_study/configs/en_all_mshr_l2_srrip.config
# 17:20 34.318 (+14.896%) Improve!!!!!
# ./regress.sh reg_re_ref_interval_aware_for_l2_srrip_again --config-file ./perf_study/configs/en_all_mshr_l2_srrip.config


# ./regress.sh reg_re_ref_interval_aware_for_l2_srrip_mshr_aware_again --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_srrip.config

# 1-22
# 29.870 (+0.000%) 
# ./regress.sh reg_mshr_disable_all_cache_rep_lru --config-file ./perf_study/configs/mshr_disable_all_cache_rep_lru.config
# 29.989 (+0.398%) ok
# ./regress.sh reg_mshr_disable_all_cache_rep_lru_line_recency --config-file ./perf_study/configs/mshr_disable_all_cache_rep_lru.config
# 16:51
# ./regress.sh reg_mshr_disable_all_cache_rep_lru_line_recency_bugfix --config-file ./perf_study/configs/mshr_disable_all_cache_rep_lru.config

# 20:43
# 29.947 (+0.210%) better (Evict smaller hits means to let totally least used lines go out)
# ./regress.sh reg_mshr_disable_all_hybrid_rep_lru_smaller_hits --config-file ./perf_study/configs/mshr_disable_all_cache_rep_lru.config
# 29.884 (+0.002%) worse
# ./regress.sh reg_mshr_disable_all_hybrid_rep_lru_larger_avg_evict_interval --config-file ./perf_study/configs/mshr_disable_all_cache_rep_lru.config

# 1-22 22:42
# 34.256 (+14.632%)
# ./regress.sh reg_mshr_independent_hybrid_rep --config-file ./perf_study/configs/mshr_independent_all_lru.config
# 34.463 (+15.324%) +0.7%
# ./regress.sh reg_mshr_en_hybrid_rep_and_mshr_aware_II --config-file ./perf_study/configs/mshr_aware_mixed_rep_l2_prime_lru.config

# 1-23 11:46 
# 34.323 (+14.845%) no help. But L1D/L2_avg_evict_interval both greatly drops. Should help but did not.
# ./regress.sh reg_mshr_aware_all_lru_enhanced_with_timestamp_hits_icnt_l2_128 --config-file ./perf_study/configs/mshr_aware_all_lru_enhanced_with_timestamp_hits_icnt_l2_128.config
# 34.323 (+14.845%)
# ./regress.sh reg_mshr_aware_all_lru_enhanced_with_timestamp_hits --config-file ./perf_study/configs/mshr_aware_all_lru_enhanced_with_timestamp_hits.config
# ./regress.sh reg_mshr_aware_all_lru --config-file ./perf_study/configs/mshr_aware_all_lru.config
# ./regress.sh reg_mshr_aware_all_lru_enhanced_with_timestamp --config-file ./perf_study/configs/mshr_aware_all_lru_enhanced_with_timestamp.config

# Modififed .config by adding rep_enhanced fields
# ./regress.sh reg_mshr_disable_all_cache_rep_lru --config-file ./perf_study/configs/mshr_disable_all_cache_rep_lru.config

################################################# regression list ##################################################
# cfg. suggestions:
# 1. MSHR en 
# mshr aware
# all lru
# (aware_mshr + l2_aware_filltime) > 
# aware_mshr > 
# l1d_aware_filltime > 
# (aware_mshr + l1d_aware_filltime) > 
# all aware_mshr_filltime

# 2. MSHR dis
# only l2_aware_filltime

# ok IPC:29.888
# ./regress.sh reg_mshr_disable_all_lru --config-file ./perf_study/configs/mshr_disable_all_lru.config
# xx
# ./regress.sh reg_mshr_en_and_aware_all_lru --config-file ./perf_study/configs/mshr_en_and_aware_all_lru.config

# baseline. re-run ok
# ./regress.sh reg_mshr_disable_l2_srrip --config-file ./perf_study/configs/mshr_disable_l2_srrip.config
# 0) re-run ok
# ./regress.sh reg_mshr_en_l2_srrip --config-file ./perf_study/configs/mshr_en_l2_srrip.config
# 1) 34.469 (+15.342%) re-run ok
# ./regress.sh reg_mshr_en__all_aware_mshr_l2_aware_filltime__l2_srrip --config-file ./perf_study/configs/mshr_en__all_aware_mshr_l2_aware_filltime__l2_srrip.config
# 2) 34.441 (+15.248%) re-run ok
# ./regress.sh reg_mshr_en__aware_mshr__l2_srrip --config-file ./perf_study/configs/mshr_en__aware_mshr__l2_srrip.config
# 3) 34.381 (+15.048%) re-run ok
# ./regress.sh reg_mshr_en__l1d_aware_filltime__l2_srrip --config-file ./perf_study/configs/mshr_en__l1d_aware_filltime__l2_srrip.config
# 4) 34.339 (+14.908%) re-run ok
# ./regress.sh reg_mshr_en__all_aware_mshr_l1d_aware_filltime__l2_srrip --config-file ./perf_study/configs/mshr_en__all_aware_mshr_l1d_aware_filltime__l2_srrip.config
# 5) 34.310 (+14.809%) re-run ok
# ./regress.sh reg_mshr_en__aware_mshr_filltime__l2_srrip --config-file ./perf_study/configs/mshr_en__aware_mshr_filltime__l2_srrip.config
# 6) 34.300 (+14.775%) re-run ok
# ./regress.sh reg_mshr_en__l2_aware_filltime__l2_srrip --config-file ./perf_study/configs/mshr_en__l2_aware_filltime__l2_srrip.config

##### all lru
# 0) 34.291 (+14.747%) re-run ok
# ./regress.sh reg_mshr_en__all_lru --config-file ./perf_study/configs/mshr_en__all_lru.config
# 1) 34.469 (+15.342%) re-run
# ./regress.sh reg_mshr_en__all_aware_mshr_l2_aware_filltime__all_lru --config-file ./perf_study/configs/mshr_en__all_aware_mshr_l2_aware_filltime__all_lru.config
# 2) 34.339 (+14.908%)
# ./regress.sh reg_mshr_en__all_aware_mshr_l1d_aware_filltime__all_lru --config-file ./perf_study/configs/mshr_en__all_aware_mshr_l1d_aware_filltime__all_lru.config
# 3) 34.484 (+15.392%)
# ./regress.sh reg_mshr_en__aware_mshr__all_lru --config-file ./perf_study/configs/mshr_en__aware_mshr__all_lru.config
# 4) 34.292 (+14.751%)
# ./regress.sh reg_mshr_en__l2_aware_filltime__all_lru --config-file ./perf_study/configs/mshr_en__l2_aware_filltime__all_lru.config
# 5) 34.462 34.462 (+15.319%)
# ./regress.sh reg_mshr_en__l1d_aware_filltime__all_lru --config-file ./perf_study/configs/mshr_en__l1d_aware_filltime__all_lru.config
# 6) 34.310 (+14.809%)
# ./regress.sh reg_mshr_en__aware_mshr_filltime__all_lru --config-file ./perf_study/configs/mshr_en__aware_mshr_filltime__all_lru.config

# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_disable_l2_srrip
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en_l2_srrip
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__all_aware_mshr_l2_aware_filltime__l2_srrip
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__all_lru
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__all_aware_mshr_l2_aware_filltime__all_lru
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__aware_mshr_total_records__all_lru
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__l2_aware_filltime__all_lru
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__aware_mshr_filltime__all_lru
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__all_aware_mshr_l1d_aware_filltime__all_lru
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__l1d_aware_filltime__all_lru
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__aware_mshr__all_lru
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__aware_mshr__l2_srrip
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__aware_mshr_filltime__l2_srrip
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__all_aware_mshr_l1d_aware_filltime__l2_srrip
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__l2_aware_filltime__l2_srrip
# ./util/job_launching/monitor_func_test.py -v -N reg_mshr_en__l1d_aware_filltime__l2_srrip

########################################### SCB/CRF Regression Script ###################################
# ::dispatch_ready_cu() for() { assert(0); }
# ./regress.sh reg_check_never_reached_branch_during_dispatch_cu --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_check_never_reached_branch_during_dispatch_cu

# 2/13 34.315 (+0.000%) -> re-run 34.246 (+0.000%) -> 3rd run 34.246 (+0.000%)
# ./regress.sh reg_baseline_default_sched --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_baseline_default_sched
# 2/15 34.177 (-0.401%) -> re-run
# ./regress.sh reg_warp_interfere_awared_schedule --config-file ./perf_study/configs/warp_interfere_awared_schedule.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_schedule

# 34.435 (+0.551%)	-> re-run 34.435 (+0.551%)
# ./regress.sh reg_warp_interfere_and_filltime_awared_cache_replace --config-file ./perf_study/configs/warp_interfere_and_filltime_awared_cache_replace.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_and_filltime_awared_cache_replace

# ./regress.sh reg_l1d_sets_16_assoc_16 --config-file ./perf_study/configs/l1d_sets_16_assoc_16.config
# ./util/job_launching/monitor_func_test.py -v -N reg_l1d_sets_16_assoc_16

# ./regress.sh reg_warp_corr_set_indexing --config-file ./perf_study/configs/warp_corr_set_indexing.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_corr_set_indexing

# ./regress.sh reg_warp_corr_set_indexing_fuck --config-file ./perf_study/configs/warp_corr_set_indexing.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_corr_set_indexing_fuck

# 34.185 (-0.229%)? drop? The same code as last submission.
# ./regress.sh reg_baseline_default_sched_II --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_baseline_default_sched_II

# src/gpgpu-sim/gpu-cache.cc
# src/gpgpu-sim/gpu-cache.h
# src/gpgpu-sim/gpu-sim.cc
# src/gpgpu-sim/shader.cc
# src/gpgpu-sim/shader.h
# 34.147 (-0.340%)	

# src/gpgpu-sim/gpu-cache.h (part)
# src/gpgpu-sim/gpu-sim.cc
# src/gpgpu-sim/shader.h
# 34.150 (-0.332%)	
# ./regress.sh reg_baseline_default_sched_II --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_baseline_default_sched_II

# src/gpgpu-sim/gpu-cache.cc
# src/gpgpu-sim/gpu-cache.h
# src/gpgpu-sim/gpu-sim.cc
# src/gpgpu-sim/shader.cc
# src/gpgpu-sim/shader.h
# 34.147 (-0.340%)
# ./regress.sh reg_baseline_default_sched_II --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_baseline_default_sched_II

# 34.166 (-0.285%)	
# ./regress.sh reg_baseline_default_sched_III --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_baseline_default_sched_III

# ./regress.sh reg_baseline_default_sched_IV --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_baseline_default_sched_IV

# 34.179 (-0.247%)
# ./regress.sh reg_warp_interfere_awared_schedule_II --config-file ./perf_study/configs/warp_interfere_awared_schedule.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_schedule_II
# 34.179 (-0.247%)
# ./regress.sh reg_warp_interfere_awared_cache_replace_II --config-file ./perf_study/configs/warp_interfere_awared_schedule.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_cache_replace_II
# 34.295 (+0.092%)
# ./regress.sh reg_warp_interfere_awared_cache_replace_bugfix --config-file ./perf_study/configs/warp_interfere_awared_schedule.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_cache_replace_bugfix

# 34.261 (-0.007%) almost the same as original reg_baseline_default_sched (IPC: 34.264)
# ./regress.sh reg_baseline_2_24 --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_baseline_2_24

# 2/24 BugFix for MSHR-awared cache replacement
# ./regress.sh reg_l1d_mshr_awared_repl --config-file ./perf_study/configs/l1d_mshr_awared_repl.config
# ./util/job_launching/monitor_func_test.py -v -N reg_l1d_mshr_awared_repl

##########################################
# ./regress.sh reg_warp_id_hashed_indexing --config-file ./perf_study/configs/warp_id_hashed_indexing.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_id_hashed_indexing

# 34.486 (+0.564%)
# ./regress.sh reg_l1d_mshr_awared_repl --config-file ./perf_study/configs/l1d_mshr_awared_repl.config
# ./util/job_launching/monitor_func_test.py -v -N reg_l1d_mshr_awared_repl

# 34.466 (+0.506%)
# ./regress.sh reg_l1d_l2_mshr_awared_repl --config-file ./perf_study/configs/l1d_l2_mshr_awared_repl.config
# ./util/job_launching/monitor_func_test.py -v -N reg_l1d_l2_mshr_awared_repl

################################ Inter-Warp Interference-Aware Cache Replace ################################
# IPC: 34.328 (+0.000%) total_issue_fails: 196939.132 (+0.000%) g_acc_r_mq_full: 4892.951 (+0.000%)
# again: 
# ./regress.sh reg_wia_cache_repl_base --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_cache_repl_base

# Running now (BugFix: Excluded "warp_id == -1" from stats for inter-warp interferences)
# 34.315 (+0.150%) 
# ./regress.sh reg_warp_interfere_awared_cache_replace_2_24 --config-file ./perf_study/configs/warp_interfere_awared_cache_replace.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_cache_replace_2_24
# 2/24 eve 34.489 (+0.659%)	highest till now
# ./regress.sh reg_warp_interfere_awared_cache_replace_fixed_mshr_corr_repl --config-file ./perf_study/configs/warp_interfere_awared_cache_replace.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_cache_replace_fixed_mshr_corr_repl

# 34.344 (+0.150%) -> 15:06 Re-run: 
# ./regress.sh reg_wia_cache_repl_l1d_mq_16 --config-file ./perf_study/configs/wia_repl_l1d_mq_16.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_cache_repl_l1d_mq_16

# 2/27 Test if L2 WIA worked
# ./regress.sh reg_test_l2_wia_worked --config-file ./perf_study/configs/l1d_l2_wia_repl_l1d_mq_16.config
# ./util/job_launching/monitor_func_test.py -v -N reg_test_l2_wia_worked

# 34.532 (+0.698%) highest with wia only
# total_issue_fails 195002.099 (-0.962%)
# ./regress.sh reg_wia_cache_repl_l1d_mq_32 --config-file ./perf_study/configs/wia_repl_l1d_mq_32.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_cache_repl_l1d_mq_32

# ./regress.sh reg_wia_two_level_active_repl_l1d_mq_32 --config-file ./perf_study/configs/wia_two_level_active_repl_l1d_mq_32.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_two_level_active_repl_l1d_mq_32
# accel-sim.out: shader.h:602: 
# two_level_active_scheduler::two_level_active_scheduler Assertion `3 == ret' failed.

# IPC: 35.213 (+2.684%)   total_issue_ratio: 3.908 (+2.920%)
# ./regress.sh reg_wia_gto_repl_l1d_mq_32 --config-file ./perf_study/configs/wia_gto_repl_l1d_mq_32.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_gto_repl_l1d_mq_32

# IPC: 35.213 (+2.684%)  total_issue_ratio: 3.908 (+2.920%)
# ./regress.sh reg_wia_rrr_repl_l1d_mq_32 --config-file ./perf_study/configs/wia_rrr_repl_l1d_mq_32.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_rrr_repl_l1d_mq_32

# IPC: 35.328 (+3.019%) total_warp_interferences:  5.022 (-99.743%) total_issue_ratio: 3.928 (+3.454%)
# ./regress.sh reg_wia_old_repl_l1d_mq_32 --config-file ./perf_study/configs/wia_old_repl_l1d_mq_32.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_old_repl_l1d_mq_32

# IPC: 35.332 (+3.030%) total_warp_interferences: 2141.575 (+9.711%)
# Guess: the majoriy of L1D trashing were saved by L2
# Try appling wia to L2 as well
# ./regress.sh reg_old_repl_l1d_mq_32 --config-file ./perf_study/configs/old_repl_l1d_mq_32.config
# ./util/job_launching/monitor_func_test.py -v -N reg_old_repl_l1d_mq_32

# ./regress.sh reg_wia_warp_limiting_repl_l1d_mq_32 --config-file ./perf_study/configs/wia_warp_limiting_repl_l1d_mq_32.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_warp_limiting_repl_l1d_mq_32
# accel-sim.out: shader.cc:2112: swl_scheduler::swl_scheduler Assertion `2 == ret' failed.

# 34.395 (+0.298%)
# ./regress.sh reg_wia_cache_repl_l1d_mq_64 --config-file ./perf_study/configs/warp_interfere_awared_cache_replace_l1d_mq_64.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_cache_repl_l1d_mq_64
# 34.378 (+0.249%) Even worse than wia only 
# total_warp_interferences 4.579 (-99.765%)->4.460 (-99.772%), but
# avg_l1d_miss_served_cycles 194792.347 180384.164 (-1.845%)->325158.812 (+76.934%)
# ./regress.sh reg_wia_mshr_aware_replace_l1d_mq_32 --config-file ./perf_study/configs/wia_mshr_aware_replace_l1d_mq_32.config
# ./util/job_launching/monitor_func_test.py -v -N reg_wia_mshr_aware_replace_l1d_mq_32


# 34.379 (+0.251%)
# ./regress.sh reg_warp_interfere_mshr_awared_cache_replace --config-file ./perf_study/configs/warp_interfere_mshr_awared_cache_replace.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_mshr_awared_cache_replace


# dead lock (It seems that smaller assoc would more likely cause LINE_ALLOC failures)
# ./regress.sh reg_warp_interfere_awared_sched_l1_sets_16_assoc_16 --config-file ./perf_study/configs/warp_interfere_awared_sched_l1_sets_16_assoc_16.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_sched_l1_sets_16_assoc_16

# 34.124 (-0.407%)
# ./regress.sh reg_warp_corr_set_indexing_fuck_II --config-file ./perf_study/configs/warp_corr_set_indexing.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_corr_set_indexing_fuck_II

# 34.422 (+0.313%)
# ./regress.sh reg_warp_interfere_mid_awared_schedule --config-file ./perf_study/configs/warp_interfere_awared_schedule.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_mid_awared_schedule
# 34.381 (+0.194%)
# ./regress.sh reg_warp_interfere_awared_schedule_075_picker --config-file ./perf_study/configs/warp_interfere_awared_schedule.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_schedule_075_picker

# ./regress.sh reg_warp_interfere_awared_schedule_050_picker --config-file ./perf_study/configs/warp_interfere_awared_schedule.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_schedule_050_picker

# 34.205 (-0.320%)
# ./regress.sh reg_warp_interfere_awared_schedule_025_picker --config-file ./perf_study/configs/warp_interfere_awared_schedule.config
# ./util/job_launching/monitor_func_test.py -v -N reg_warp_interfere_awared_schedule_025_picker

# ./regress.sh reg_sched_warp_when_interference_below_3 --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_sched_warp_when_interference_below_3

# 29.465 (+2.826%)
# ./regress.sh reg_sched_warp_when_interference_below_5 --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_sched_warp_when_interference_below_5
# 34.455 (+0.410%) higher than "below_20"
# ./regress.sh reg_sched_warp_when_interference_below_10 --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_sched_warp_when_interference_below_10
# 34.436 (+0.353%)
# ./regress.sh reg_sched_warp_when_interference_below_20 --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_sched_warp_when_interference_below_20

# ./regress.sh reg_profile_warp_interference --config-file ./perf_study/configs/warp_schedule_base.config
# ./util/job_launching/monitor_func_test.py -v -N reg_profile_warp_interference

# ./regress.sh reg_max_insn_issue_per_warp_2 --config-file ./perf_study/configs/max_insn_issue_per_warp_2.config
# ./util/job_launching/monitor_func_test.py -v -N reg_max_insn_issue_per_warp_2

# ./regress.sh reg_expand_int_resource --config-file ./perf_study/configs/expand_int_resource.config
# ./util/job_launching/monitor_func_test.py -v -N reg_expand_int_resource

# ./regress.sh reg_num_eu_8__num_sched_per_core_8__max_insn_issue_per_warp_1 --config-file ./perf_study/configs/num_eu_8__num_sched_per_core_8__max_insn_issue_per_warp_1.config
# ./util/job_launching/monitor_func_test.py -v -N reg_num_eu_8__num_sched_per_core_8__max_insn_issue_per_warp_1

# ./regress.sh reg_num_eu_16__num_sched_per_core_16__opc_16__max_insn_issue_per_warp_1 --config-file ./perf_study/configs/num_eu_16__num_sched_per_core_16__opc_16__max_insn_issue_per_warp_1.config
# ./util/job_launching/monitor_func_test.py -v -N reg_num_eu_16__num_sched_per_core_16__opc_16__max_insn_issue_per_warp_1

# ./regress.sh reg_num_eu_64__num_sched_per_core_64__opc_64__max_insn_issue_per_warp_1 --config-file ./perf_study/configs/num_eu_64__num_sched_per_core_64__opc_64__max_insn_issue_per_warp_1.config
# ./util/job_launching/monitor_func_test.py -v -N reg_num_eu_64__num_sched_per_core_64__opc_64__max_insn_issue_per_warp_1

# ./regress.sh reg_num_eu_8__num_sched_per_core_8__max_insn_issue_per_warp_2 --config-file ./perf_study/configs/num_eu_8__num_sched_per_core_8__max_insn_issue_per_warp_2.config
# ./util/job_launching/monitor_func_test.py -v -N reg_num_eu_8__num_sched_per_core_8__max_insn_issue_per_warp_2

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
  if [ -n "$CUSTOM_CFG_FILE" ]; then
    if [ ! -f "$CUSTOM_CFG_FILE" ]; then
      echo "[ERROR] --config-file 路径不存在: $CUSTOM_CFG_FILE"; exit 1
    fi
    export CUSTOM_GPGPUSIM_CONFIG="$CUSTOM_CFG_FILE"
    echo "[INFO] Group 模式使用自定义 gpgpusim.config (环境变量方式): $CUSTOM_CFG_FILE"
  fi
  echo "[INFO] Group 回归: variant_tag=$VARIANT_TAG"
  EXTRA_ARGS=("${REM_ARGS[@]}")
  CMD=(
    python3 util/job_launching/run_simulations.py
    -B rodinia_2.0-ft
    -C "${RUN_CFG:-QV100-SASS}"
    -T ~/dev/accel-sim/accel-sim-framework/hw_run/rodinia_2.0-ft/11.0
    --variant_tag "$VARIANT_TAG"
  )
  CMD+=("${EXTRA_ARGS[@]}")
  CMD+=(-N "$VARIANT_TAG")
  "${CMD[@]}"
fi

# # L1D 统一容量为 64KB（示例：l1d64）
# python3 util/job_launching/run_simulations.py \
#   -B rodinia_2.0-ft \
#   -C QV100-SASS \
#   -T ~/dev/accel-sim/accel-sim-framework/hw_run/rodinia_2.0-ft/11.0 \
#   --variant_tag l1d64 \
#   --extra_sim_params '-gpgpu_unified_l1d_size 64' \
#   -N reg-l1d64-2025-1031

# # 跳过 L1D（显著改动：global memory 访问绕过 L1D）
# python3 util/job_launching/run_simulations.py \
#   -B rodinia_2.0-ft \
#   -C QV100-SASS \
#   -T ~/dev/accel-sim/accel-sim-framework/hw_run/rodinia_2.0-ft/11.0 \
#   --variant_tag skipL1D \
#   --extra_sim_params ' -gpgpu_unified_l1d_size 64 -gpgpu_gmem_skip_L1D 1' \
#   -N reg-skipL1D-2025-1031
