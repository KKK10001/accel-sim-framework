python3 util/job_launching/aggregate_ipc.py \
  -R ./sim_run_12.1 \
  -C QV100-SASS \
  -N reg-baseline-2025-1031 \
  -o util/job_launching/ipc_reg-baseline-2025-1031.csv \
  -p ""  # 不在聚合阶段出图

python3 util/job_launching/aggregate_ipc.py \
  -R ./sim_run_12.1 \
  -C QV100-SASS \
  -N reg-l1d64-2025-1031 \
  -o util/job_launching/ipc_reg-l1d64-2025-1031.csv \
  -p ""

  python3 util/job_launching/aggregate_ipc.py \
  -R ./sim_run_12.1 \
  -C QV100-SASS \
  -N reg-skipL1D-2025-1031 \
  -o util/job_launching/ipc_reg-skipL1D-2025-1031.csv \
  -p ""

# 画图
# 基线 vs l1d64:
python3 util/job_launching/plot_compare_policies.py \
  --baseline util/job_launching/ipc_reg-baseline-2025-1031.csv \
  --variant  util/job_launching/ipc_reg-l1d64-2025-1031.csv \
  --out-dir /home/hjs/dev/accel-sim/accel-sim-framework/sim_run_12.1/draws \
  --bench-only

# 基线 vs skipL1D:
python3 util/job_launching/plot_compare_policies.py \
  --baseline util/job_launching/ipc_reg-baseline-2025-1031.csv \
  --variant  util/job_launching/ipc_reg-skipL1D-2025-1031.csv \
  --out-dir /home/hjs/dev/accel-sim/accel-sim-framework/sim_run_12.1/draws \
  --bench-only


# 输出文件固定命名为：

# grouped_ipc.png
# grouped_l2_bw.png
# grouped_l2_total_cache_miss_rate.png
# 同时会在 out-dir 下写出 grouped_delta.csv(方便对比每个用例的 base/var 数值与 delta/pct)

