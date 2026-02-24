#!/bin/bash

# 检查输入文件
if [ $# -lt 1 ]; then
    echo "用法: $0 <文件名>"
    exit 1
fi

input_file="$1"  # perf_rpt.o

# 查找第一次出现 warp_interfere[ 的行号
start_line=$(grep -n "warp_interfere\[" "$input_file" | head -1 | cut -d: -f1)

# 查找 per_core_warp_interferences[sid:0 的前两次出现行号
per_core_lines=$(grep -n "per_core_warp_interferences\[sid:0" "$input_file" | cut -d: -f1)
first_per_core_line=$(echo "$per_core_lines" | sed -n '1p')
second_per_core_line=$(echo "$per_core_lines" | sed -n '2p')

# 默认使用第一次出现
end_line="$first_per_core_line"

# 若第一次 per_core 出现在首次 warp_interfere 之前，说明跨 kernel，改用第二次 per_core
if [ -n "$start_line" ] && [ -n "$first_per_core_line" ] && [ "$first_per_core_line" -lt "$start_line" ]; then
    end_line="$second_per_core_line"
fi

# 检查是否都找到
if [ -z "$start_line" ] || [ -z "$end_line" ]; then
    echo "错误: 未找到指定的字符串"
    exit 1
fi

if [ "$end_line" -lt "$start_line" ]; then
    echo "错误: 结束行早于起始行 (start=$start_line, end=$end_line)"
    exit 1
fi

# 提取两个行号之间的内容
sed -n "$start_line,$((end_line - 1)) p" "$input_file" > warp_interfere_output

awk -F 'sid:|\\]' '{file="sid_"$2"_warp_interfere.txt"; print > file}' warp_interfere_output
