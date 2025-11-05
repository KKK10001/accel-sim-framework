#!/usr/bin/env bash
# 清理由 regress_with_ptx.sh 生成的 variant_tag 目录。支持直接指定
# variant_tag，或在无参数时列出已检测到的 variant_tag 并提示选择单个
# 目标进行删除。

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# 回退到脚本所在的 accel-sim-framework 目录，保证 --help 等功能在
# 未设置环境变量时也能使用。
if [[ -z "${ACCELSIM_ROOT:-}" ]]; then
  ACCELSIM_ROOT="$script_dir"
fi

print_help() {
  cat <<'EOF'
Usage: clean_with_ptx.sh [variant_tag] [options]

默认行为：扫描 sim_run_* 目录，列出检测到的 variant_tag，并提示选取其
中一个进行清理。若直接传入 variant_tag，则跳过列出阶段。

Options:
  -y, --yes   跳过确认提示，直接删除匹配目录
  -h, --help  显示本说明并退出

示例：
  ./clean_with_ptx.sh baseline_20251104_093411
  ./clean_with_ptx.sh --yes baseline_20251104_093411
  ./clean_with_ptx.sh   # 交互式选择 variant_tag
EOF
}

confirm="false"
declared_variant=""
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
    -*)
      echo "ERROR: 未知选项 $1" >&2
      exit 1
      ;;
    *)
      positional+=("$1")
      shift
      ;;
  esac
done

if [[ ${#positional[@]} -gt 1 ]]; then
  echo "ERROR: 目前仅支持 0 或 1 个 variant_tag 参数" >&2
  exit 1
fi

declared_variant="${positional[0]:-}"

trim_whitespace() {
  local value="$1"
  # 去除首尾空白字符（兼容 Bash 字符类写法）。
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

workspace_root=$(cd "$ACCELSIM_ROOT/.." && pwd)

mapfile -t run_roots < <(
  find "$workspace_root" -maxdepth 1 -type d -name 'sim_run_*' 2>/dev/null \
    | LC_ALL=C sort
)

if ((${#run_roots[@]} == 0)); then
  echo "未找到任何 sim_run_* 目录，似乎没有可清理的运行结果" >&2
  exit 0
fi

declare -a VARIANT_TAGS=()

gather_variant_tags() {
  local -a tags=()
  mapfile -t tags < <(
    for root in "${run_roots[@]}"; do
      find "$root" -mindepth 5 -maxdepth 5 -type d 2>/dev/null
    done | awk -F'/' '{print $NF}' | LC_ALL=C sort -u
  )
  VARIANT_TAGS=("${tags[@]}")
}

select_variant_tag() {
  if [[ -n "$declared_variant" ]]; then
    return
  fi

  gather_variant_tags
  if ((${#VARIANT_TAGS[@]} == 0)); then
    echo "未检测到任何 variant_tag 目录" >&2
    exit 0
  fi

  echo "检测到的 variant_tag："
  for tag in "${VARIANT_TAGS[@]}"; do
    printf '  %s\n' "$tag"
  done

  read -rp "输入要清理的 variant_tag (留空取消): " user_choice
  user_choice=$(trim_whitespace "$user_choice")
  if [[ -z "$user_choice" ]]; then
    echo "已取消"
    exit 0
  fi

  declared_variant="$user_choice"
}

select_variant_tag

declared_variant=$(trim_whitespace "$declared_variant")

if [[ -z "$declared_variant" ]]; then
  echo "ERROR: variant_tag 不能为空" >&2
  exit 1
fi

if [[ -z "${declared_variant//[^A-Za-z0-9_]/}" ]]; then
  echo "警告: variant_tag '$declared_variant' 看起来异常，请确认输入是否正确" >&2
fi

mapfile -t target_dirs < <(
  for root in "${run_roots[@]}"; do
    find "$root" -mindepth 5 -maxdepth 5 -type d -name "$declared_variant" 2>/dev/null
  done | LC_ALL=C sort
)

if ((${#target_dirs[@]} == 0)); then
  echo "未找到名为 '$declared_variant' 的 variant_tag 目录" >&2
  exit 0
fi

echo "即将删除以下目录："
for dir in "${target_dirs[@]}"; do
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

for dir in "${target_dirs[@]}"; do
  rm -rf -- "$dir"
  echo "已删除 $dir"
  # 清理潜在的空父目录。
  parent=$(dirname "$dir")
  find "$parent" -type d -empty -delete >/dev/null 2>&1 || true
done

# 清理 sim_run_* 下的空目录，保持树结构整洁。
for root in "${run_roots[@]}"; do
  find "$root" -type d -empty -delete >/dev/null 2>&1 || true
done

echo "完成"
