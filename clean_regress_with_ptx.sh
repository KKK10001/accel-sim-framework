#!/usr/bin/env bash
# Remove Accel-Sim GPU_Microbenchmark regression outputs that match the
# variant_tag used by regress_with_ptx.sh. Mirrors the target selection logic
# so you can safely clean either the whole suite or a single microbenchmark.

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if [[ -z "${ACCELSIM_ROOT:-}" ]]; then
  ACCELSIM_ROOT="$script_dir"


confirm="false"
args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -y|--yes)
      confirm="true"
      shift
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    --)
      shift
      args+=("$@")
      break
      ;;
    -* )
      echo "ERROR: 未知选项 $1" >&2
      exit 1
      ;;
    * )
      args+=("$1")
      shift
      ;;
  esac
done

if [[ ${#args[@]} -gt 1 ]]; then
  echo "ERROR: 目前仅支持 0 或 1 个 microbenchmark 参数" >&2
  exit 1
fi

target_input="${args[0]:-GPU_Microbenchmark}"
microbenchmark 名（如 l1_bw_128 或 GPU_Microbenchmark:l1_bw_128）时只会
清理对应的条目。

--yes      跳过确认，直接执行删除。
--help     显示本说明。

可选的 L1/L2 microbenchmark 名单：
EOF
  if ((${#CACHE_TARGETS[@]} == 0)); then
    if [[ -n "$ubench_root" ]]; then
      echo "  (在 $ubench_root 下未找到 l1_cache/l2_cache 子目录)"
    else
      echo "  (未能定位 GPU_Microbenchmark ubench 目录，请确认 GPUAPPS_ROOT)"
    fi
  else
    for name in "${CACHE_TARGETS[@]}"; do
      printf '  %s\n' "$name"
    done
  fi
}

confirm="false"
positional=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -y|--yes)
      confirm="true"
      shift
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    --)
      shift
      positional+=("$@")
      break
      ;;
    -* )
      echo "ERROR: 未知选项 $1" >&2
      exit 1
      ;;
    * )
      positional+=("$1")
      shift
      ;;
  esac
  if [[ "$1" == "--" ]]; then
    continue
  fi
  if [[ ${#positional[@]} -gt 1 ]]; then
    echo "ERROR: 目前仅支持 0 或 1 个 microbenchmark 参数" >&2
    exit 1
  fi
done

if [[ ${#positional[@]} -gt 1 ]]; then
  echo "ERROR: 目前仅支持 0 或 1 个 microbenchmark 参数" >&2
  exit 1
fi

target_input="${positional[0]:-GPU_Microbenchmark}"
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

launch_stub="${target_suite//[: ,]/_}"
feature="baseline"
variant_tag="${target_suite}_${feature}"

echo "variant_tag: $variant_tag"

if ! command -v nvcc >/dev/null 2>&1; then
  echo "ERROR: nvcc 未找到，无法推断 CUDA 版本" >&2
  exit 1
fi

cuda_version=$(nvcc --version | grep release | head -n1 | sed -re 's/.*release ([0-9]+\.[0-9]+).*/\1/')
if [[ -z "$cuda_version" ]]; then
  echo "ERROR: 未能解析 CUDA 版本" >&2
  exit 1
fi

run_root=$(cd "$ACCELSIM_ROOT/.." && pwd)/sim_run_${cuda_version}
if [[ ! -d "$run_root" ]]; then
  echo "未找到运行目录 $run_root，无需清理" >&2
  exit 0
fi

mapfile -t candidate_dirs < <(find "$run_root" -type d -name "$variant_tag" 2>/dev/null | LC_ALL=C sort)

if [[ ${#candidate_dirs[@]} -eq 0 ]]; then
  echo "未找到匹配 variant_tag=$variant_tag 的目录" >&2
  exit 0
fi

echo "即将删除以下目录："
for dir in "${candidate_dirs[@]}"; do
  printf '  %s\n' "$dir"
done

if [[ "$confirm" != "true" ]]; then
  read -rp "确认删除? [y/N] " reply
  case "$reply" in
    y|Y|yes|YES)
      ;;
    *)
      echo "已取消"
      exit 0
      ;;
  esac
fi

for dir in "${candidate_dirs[@]}"; do
  rm -rf -- "$dir"
  echo "已删除 $dir"
done

# 清理可能留下的空目录层级。
find "$run_root" -type d -empty -delete >/dev/null 2>&1 || true

echo "完成"
