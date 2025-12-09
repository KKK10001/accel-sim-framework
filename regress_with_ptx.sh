# ./util/job_launching/run_simulations.py -B rodinia_2.0-ft -C QV100-SASS -T ./hw_run/traces/device-0/12.1/ -N regtest-2025-10-30-1538
ACCEL_SIM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$ACCEL_SIM_DIR"

# 多个改动可以一起写在 --extra_sim_params 的同一对引号里，用空格分隔。例如：' -gpgpu_unified_l1d_size 64 -gpgpu_gmem_skip_L1D 1 '
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Fall back to repo layout when environment variables are missing so that --help still works.
if [[ -z "${ACCELSIM_ROOT:-}" ]]; then
  ACCELSIM_ROOT="$script_dir"
fi

gpuapps_root="${GPUAPPS_ROOT:-}"
if [[ -z "$gpuapps_root" && -d "$ACCELSIM_ROOT/../gpu-app-collection" ]]; then
  gpuapps_root=$(cd "$ACCELSIM_ROOT/../gpu-app-collection" && pwd)
fi

declare -a APPS_YAML_CANDIDATES=(
  "$ACCELSIM_ROOT/util/job_launching/apps/define-all-apps.yml"
  "$ACCELSIM_ROOT/../util/job_launching/apps/define-all-apps.yml"
)

apps_yaml=""
for candidate in "${APPS_YAML_CANDIDATES[@]}"; do
  if [[ -f "$candidate" ]]; then
    apps_yaml="$candidate"
    break
  fi
done

preferred_yaml="${APPS_YAML_CANDIDATES[0]}"

gather_cache_targets() {
  local yaml_path="$1"
  python3 - "$yaml_path" <<'PY' || true
import sys
from pathlib import Path

yaml_path = Path(sys.argv[1])
if not yaml_path.is_file():
    sys.exit(0)

names = []
in_section = False
in_execs = False
section_indent = None
execs_indent = None

with yaml_path.open(encoding="utf-8") as handle:
    for raw in handle:
        line = raw.rstrip("\n")
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(stripped)

        if not in_section:
            if stripped == "GPU_Microbenchmark:":
                in_section = True
                section_indent = indent
            continue

        if indent <= section_indent and not stripped.startswith("#"):
            break

        if not in_execs:
            if stripped.startswith("execs:"):
                in_execs = True
                execs_indent = indent
            continue

        if indent <= execs_indent and not stripped.startswith("#"):
            break

        if not stripped.startswith('- '):
            continue

        if execs_indent is None:
            continue

        if indent != execs_indent + 4:
            continue

        candidate = stripped[2:]
        if candidate.endswith(':'):
            candidate = candidate[:-1]
        candidate = candidate.strip()
        if candidate and not candidate.startswith('#'):
            names.append(candidate)

for name in sorted(set(names)):
    print(name)
PY
}

declare -a CACHE_TARGETS=()
if [[ -n "$apps_yaml" ]]; then
  readarray -t CACHE_TARGETS < <(gather_cache_targets "$apps_yaml")
fi

cache_targets_note=""
if [[ -z "$apps_yaml" ]]; then
  cache_targets_note="  (未找到 $preferred_yaml，请确认 ACCELSIM_ROOT 环境变量)"
elif ((${#CACHE_TARGETS[@]} == 0)); then
  cache_targets_note="  (在 $apps_yaml 中没有列出任何 GPU_Microbenchmark 条目)"
fi

print_help() {
  local script_name
  script_name=$(basename "$0")
  cat <<EOF
Usage: $script_name [microbenchmark]

省略参数时会提交整个 GPU_Microbenchmark 套件。
传入单个名字（如 l1_bw_128）将自动映射为 GPU_Microbenchmark:<name>。
也可以直接使用完整形式 GPU_Microbenchmark:<name>。

可选的 L1/L2 microbenchmark 名单：
EOF
  if ((${#CACHE_TARGETS[@]} == 0)); then
    echo "$cache_targets_note"
  else
    for name in "${CACHE_TARGETS[@]}"; do
      printf '  %s\n' "$name"
    done
  fi
}

if [[ $# -gt 1 ]]; then
  echo "ERROR: 目前仅支持 0 或 1 个参数；使用 --help 查看用法" >&2
  exit 1
fi

if [[ $# -gt 0 ]]; then
  case "$1" in
    -h|--help)
      print_help
      exit 0
      ;;
  esac
fi

target_input="${1:-GPU_Microbenchmark}"
target_suite="$target_input"
micro_requested=""

if [[ "$target_input" == "GPU_Microbenchmark" ]]; then
  target_suite="GPU_Microbenchmark"
elif [[ "$target_input" == GPU_Microbenchmark:* ]]; then
  micro_requested="${target_input#GPU_Microbenchmark:}"
else
  micro_requested="$target_input"
  target_suite="GPU_Microbenchmark:${micro_requested}"
fi

if [[ -n "$micro_requested" && ${#CACHE_TARGETS[@]} -gt 0 ]]; then
  found=0
  for name in "${CACHE_TARGETS[@]}"; do
    if [[ "$name" == "$micro_requested" ]]; then
      found=1
      break
    fi
  done
  if [[ $found -eq 0 ]]; then
    echo "ERROR: 未识别的 microbenchmark '$micro_requested'；使用 $0 --help 查看可选列表" >&2
    exit 1
  fi
fi

cd "$ACCELSIM_ROOT/.."
echo "$PWD=$PWD"

launch_stub="${target_suite//[: ,]/_}"
timestamp=$(date +%Y%m%d_%H%M%S)
feature="baseline"
launch_name="run_${launch_stub}_${feature}_${timestamp}"
variant_tag="${feature}_${timestamp}"
# variant_tag="${target_suite}"

echo "launch_name: $launch_name"
echo "variant_tag: $variant_tag"

# 基线回归(base_config/baseline，无额外改动)
python3 "$ACCEL_SIM_DIR/util/job_launching/run_simulations.py" \
  -B "$target_suite" \
  -C QV100 \
  --variant_tag "$variant_tag" \
  -N "$launch_name"

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
