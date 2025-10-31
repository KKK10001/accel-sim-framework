# ./util/job_launching/run_simulations.py -B rodinia_2.0-ft -C QV100-SASS -T ./hw_run/traces/device-0/12.1/ -N regtest-2025-10-30-1538

# 多个改动可以一起写在 --extra_sim_params 的同一对引号里，用空格分隔。例如：' -gpgpu_unified_l1d_size 64 -gpgpu_gmem_skip_L1D 1 '
cd $ACCELSIM_ROOT/..
echo "$PWD="$PWD
# 基线回归(base_config/baseline，无额外改动)
python3 util/job_launching/run_simulations.py \
  -B rodinia_2.0-ft \
  -C QV100-SASS \
  -T /home/kuanbba/dev/accel-sim/accel-sim-framework/hw_run/traces/device-0 \
  --variant_tag baseline \
  -N reg-baseline-2025-1031

# L1D 统一容量为 64KB（示例：l1d64）
python3 util/job_launching/run_simulations.py \
  -B rodinia_2.0-ft \
  -C QV100-SASS \
  -T /home/kuanbba/dev/accel-sim/accel-sim-framework/hw_run/traces/device-0 \
  --variant_tag l1d64 \
  --extra_sim_params '-gpgpu_unified_l1d_size 64' \
  -N reg-l1d64-2025-1031

# 跳过 L1D（显著改动：global memory 访问绕过 L1D）
python3 util/job_launching/run_simulations.py \
  -B rodinia_2.0-ft \
  -C QV100-SASS \
  -T /home/kuanbba/dev/accel-sim/accel-sim-framework/hw_run/traces/device-0 \
  --variant_tag skipL1D \
  --extra_sim_params ' -gpgpu_unified_l1d_size 64 -gpgpu_gmem_skip_L1D 1' \
  -N reg-skipL1D-2025-1031
