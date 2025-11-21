#!/usr/bin/env python3
"""
plot_benchmark_fail_stats.py

Generates per-benchmark bar charts comparing base vs feature configs over kernels.

Structure expected (per benchmark):
  sim_run_<cuda_ver>/<benchmark>/<args_subdir>/QV100-SASS/<variant_tag>/*.o

Assumptions:
  - Each variant directory contains at least one .o file; newest (mtime) chosen.
  - Each .o file prints 'gpu_ipc =' once per kernel in order of execution.
  - For each kernel region, lines of the form:
        Total_core_cache_fail_stats_breakdown[GLOBAL_ACC_R] = <total_r>
        Total_core_cache_fail_stats_breakdown[GLOBAL_ACC_R][<REASON>] = <count>
    (similar GLOBAL_ACC_W) appear after or near the ipc line. We collect the most
    recent seen stats for that kernel.

If fail stats only appear once at file end (aggregated), they will be applied to
all kernels uniformly (still allowing visual comparison of IPC vs total fails).

Bars per kernel per config (grouped):
  - gpu_ipc (solid color)
  - Total_core_cache_fail_stats_breakdown[GLOBAL_ACC_R] (stacked by reasons, hatched)
  - Total_core_cache_fail_stats_breakdown[GLOBAL_ACC_W] (stacked by reasons, hatched with different patterns)

Usage example (explicit sim-root):
    python perf_study/plot/plot_benchmark_fail_stats.py \
        --sim-root /abs/path/to/sim_run_12.1 \
        --benchmarks backprop-rodinia-2.0-ft bfs-rodinia-2.0-ft streamcluster-rodinia-2.0-ft \
        --variants regress-default-config regress-mshr-entries-32-again \
        --output-dir ./perf_study/plot

If --sim-root is omitted, attempts to use "$ACCELSIM_ROOT/../sim_run_12.1" automatically.

Output: <output-dir>/<benchmark>.png
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from typing import List, Dict, Tuple

import matplotlib
# Force non-interactive backend for headless environments (no X server)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GPU_IPC_RE = re.compile(r"gpu_ipc\s*=\s*([0-9]+\.?[0-9]*)")
TOTAL_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\s*=\s*([0-9]+)")
TOTAL_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\s*=\s*([0-9]+)")
CAUSE_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\[(.+?)\]\s*=\s*([0-9]+)")
CAUSE_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\[(.+?)\]\s*=\s*([0-9]+)")

def pick_latest_o_file(variant_dir: str) -> str:
    # Accept files ending with .o or .o<digits> (simulation output naming)
    pat = re.compile(r".*\.o(\d+)?$")
    candidates = [os.path.join(variant_dir, f) for f in os.listdir(variant_dir) if pat.match(f)]
    if not candidates:
        return ''
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]

def parse_o_file(path: str):
    """Parse an .o file returning per-kernel records.
    Returns list of dicts: [{'ipc':float,'r_total':int,'r_reasons':{..},'w_total':int,'w_reasons':{..}}]
    If totals appear only once, they are applied to all kernels.
    """
    try:
        text = open(path).read().splitlines()
    except Exception as e:
        print(f"[WARN] Could not read {path}: {e}")
        return []

    kernels = []
    current = None
    last_r_total = 0
    last_w_total = 0
    last_r_reasons: Dict[str,int] = {}
    last_w_reasons: Dict[str,int] = {}

    def commit_kernel():
        if current is not None:
            # Attach the latest fail stats snapshot
            current['r_total'] = last_r_total
            current['w_total'] = last_w_total
            current['r_reasons'] = dict(last_r_reasons)
            current['w_reasons'] = dict(last_w_reasons)
            kernels.append(current)

    for line in text:
        m_ipc = GPU_IPC_RE.search(line)
        if m_ipc:
            # Starting a new kernel record
            commit_kernel()
            current = {'ipc': float(m_ipc.group(1))}
            continue
        m_tr = TOTAL_R_RE.search(line)
        if m_tr:
            last_r_total = int(m_tr.group(1))
            continue
        m_tw = TOTAL_W_RE.search(line)
        if m_tw:
            last_w_total = int(m_tw.group(1))
            continue
        m_cr = CAUSE_R_RE.search(line)
        if m_cr:
            last_r_reasons[m_cr.group(1)] = int(m_cr.group(2))
            continue
        m_cw = CAUSE_W_RE.search(line)
        if m_cw:
            last_w_reasons[m_cw.group(1)] = int(m_cw.group(2))
            continue

    commit_kernel()
    # If no kernel boundaries found but we have totals, fabricate single kernel
    if not kernels and (last_r_total or last_w_total):
        kernels = [{
            'ipc': None,
            'r_total': last_r_total,
            'w_total': last_w_total,
            'r_reasons': dict(last_r_reasons),
            'w_reasons': dict(last_w_reasons)
        }]
    return kernels

def collect_benchmark(sim_root: str, benchmark: str, variants: List[str]) -> Dict[str,List[Dict]]:
    """Return mapping variant -> list[kernel_records].
    We search benchmark sub-tree for variant_tag directories under QV100-SASS.
    """
    bench_dir = os.path.join(sim_root, benchmark)
    if not os.path.isdir(bench_dir):
        print(f"[WARN] benchmark dir missing: {bench_dir}")
        return {}
    variant_data = {}
    # search arg subdirs
    for args_sub in os.listdir(bench_dir):
        args_path = os.path.join(bench_dir, args_sub, 'QV100-SASS')
        if not os.path.isdir(args_path):
            continue
        for var in variants:
            vdir = os.path.join(args_path, var)
            if not os.path.isdir(vdir):
                continue
            ofile = pick_latest_o_file(vdir)
            if not ofile:
                print(f"[WARN] no .o file for {benchmark} variant {var} at {vdir}")
                continue
            kernels = parse_o_file(ofile)
            variant_data[var] = kernels
    return variant_data

def ensure_same_kernel_count(variant_data: Dict[str,List[Dict]]) -> int:
    counts = {v: len(variant_data[v]) for v in variant_data}
    if not counts:
        return 0
    maxc = max(counts.values())
    # Pad shorter lists with None placeholders (so bars align)
    for v, c in counts.items():
        if c < maxc:
            last = variant_data[v][-1] if variant_data[v] else {'ipc':None,'r_total':0,'w_total':0,'r_reasons':{},'w_reasons':{}}
            for _ in range(maxc - c):
                variant_data[v].append(last)
    return maxc

def plot_benchmark(benchmark: str, variant_data: Dict[str,List[Dict]], variants: List[str], out_dir: str):
    if not variant_data:
        print(f"[INFO] Skip benchmark {benchmark}, no data")
        return
    kernel_count = ensure_same_kernel_count(variant_data)
    if kernel_count == 0:
        print(f"[INFO] Skip benchmark {benchmark}, zero kernels")
        return
    # Prepare figure with dual y-axis: left for IPC, right for fail counts
    fig, ax_ipc = plt.subplots(figsize=(max(6, kernel_count*1.2), 6))
    ax_fail = ax_ipc.twinx()

    # New layout: For each kernel we define 3 metric groups (IPC, ReadFail, WriteFail).
    # Within each metric group, variants are placed side-by-side adjacently (base next to feature).
    kernel_span = 0.9
    metric_groups = 3  # IPC, Read, Write
    group_span = kernel_span / metric_groups
    variant_count = max(1, len(variants))
    # Each group subdivided equally for variant bars
    variant_span = group_span / variant_count
    inner_gap = variant_span * 0.15
    bar_width = variant_span - inner_gap
    # Colors (by original variant tag key)
    variant_colors = {variants[0]: '#1f77b4'}
    if len(variants) > 1:
        variant_colors[variants[1]] = '#d62728'
    # Hatches per reason
    read_hatches_cycle = ['/', '\\', 'x', '-', '+', '.']
    write_hatches_cycle = ['.', '||', '++', 'oo']

    # Collect all reasons to maintain deterministic hatch assignment
    all_read_reasons = []
    all_write_reasons = []
    for v in variants:
        for krec in variant_data.get(v, []):
            for r in krec['r_reasons'].keys():
                if r not in all_read_reasons:
                    all_read_reasons.append(r)
            for r in krec['w_reasons'].keys():
                if r not in all_write_reasons:
                    all_write_reasons.append(r)
    read_hatches = {r: read_hatches_cycle[i % len(read_hatches_cycle)] for i, r in enumerate(all_read_reasons)}
    write_hatches = {r: write_hatches_cycle[i % len(write_hatches_cycle)] for i, r in enumerate(all_write_reasons)}

    x_positions = list(range(kernel_count))
    # Optional debug: print chosen .o file summary once per variant (first kernel only)
    if os.getenv('PLOT_DEBUG', '0') == '1':
        print(f"[DEBUG] Plotting benchmark {benchmark} with variants: {variants}")
    # Draw bars grouped by metric, variants adjacent within each group
    for ki in range(kernel_count):
        base_x = x_positions[ki]
        kernel_left = base_x - kernel_span/2
        for group_index, metric in enumerate(['ipc', 'r', 'w']):
            group_left = kernel_left + group_index * group_span
            for vi, v in enumerate(variants):
                krec_list = variant_data.get(v, [])
                if ki >= len(krec_list):
                    continue
                krec = krec_list[ki]
                x_bar_left = group_left + vi * variant_span + inner_gap/2
                if metric == 'ipc':
                    if krec.get('ipc') is not None:
                        ax_ipc.bar(x_bar_left + bar_width/2, krec['ipc'], width=bar_width, color=variant_colors[v])
                elif metric == 'r':
                    r_total = krec.get('r_total', 0)
                    if r_total > 0:
                        bottom = 0
                        for reason, val in sorted(krec['r_reasons'].items(), key=lambda kv: kv[0]):
                            if val == 0: continue
                            ax_fail.bar(x_bar_left + bar_width/2, val, width=bar_width, bottom=bottom, color=variant_colors[v], hatch=read_hatches.get(reason,'/'), edgecolor='black')
                            bottom += val
                elif metric == 'w':
                    w_total = krec.get('w_total', 0)
                    if w_total > 0:
                        bottom = 0
                        for reason, val in sorted(krec['w_reasons'].items(), key=lambda kv: kv[0]):
                            if val == 0: continue
                            ax_fail.bar(x_bar_left + bar_width/2, val, width=bar_width, bottom=bottom, color=variant_colors[v], hatch=write_hatches.get(reason,'.'), edgecolor='black')
                            bottom += val

    ax_ipc.set_xticks(x_positions)
    ax_ipc.set_xticklabels([f'kernel-{i+1}' for i in range(kernel_count)], rotation=30)
    ax_ipc.set_ylabel('gpu_ipc')
    ax_fail.set_ylabel('Fail counts (Read/Write)')
    # Move overall title to figure top so it does not conflict with in-axes legend
    fig.suptitle(f'{benchmark}', y=0.97)
    # Build legend without duplicates
    # Build custom legend with requested layout (3 rows x 2 columns)
    from matplotlib.patches import Patch

    def norm_variant_name(tag: str) -> str:
        name = tag
        if name.startswith('regress-'):
            name = name[len('regress-'):]
        if name.endswith('-again'):
            name = name[:-len('-again')]
        if name == 'default-config':
            return 'base-config'
        return name

    # We only display two variants side-by-side as specified
    disp_variants = variants[:2]
    # Prepare handles for 3 rows x 2 columns
    handles = []
    labels = []
    # Row 1: IPC
    for v in disp_variants:
        handles.append(Patch(facecolor=variant_colors.get(v, '#999999')))
        labels.append(f"IPC: {norm_variant_name(v)}")
    # Determine hatches for MISS_QUEUE_FULL (read/write)
    rq_hatch = read_hatches.get('MISS_QUEUE_FULL', '/')
    wq_hatch = write_hatches.get('MISS_QUEUE_FULL', '.')
    # Row 2: rd MISS_QUEUE_FULL
    for v in disp_variants:
        handles.append(Patch(facecolor=variant_colors.get(v, '#999999'), hatch=rq_hatch, edgecolor='black'))
        labels.append(f"rd MISS_QUEUE_FULL: {norm_variant_name(v)}")
    # Row 3: wr MISS_QUEUE_FULL
    for v in disp_variants:
        handles.append(Patch(facecolor=variant_colors.get(v, '#999999'), hatch=wq_hatch, edgecolor='black'))
        labels.append(f"wr MISS_QUEUE_FULL: {norm_variant_name(v)}")

    if handles:
        ax_ipc.legend(
            handles,
            labels,
            fontsize='x-small',
            ncol=2,
            loc='upper left',
            bbox_to_anchor=(0.0, 1.0, 1.0, 0.01),
            bbox_transform=ax_ipc.transAxes,
            mode='expand',
            frameon=True,
            borderaxespad=0.2,
            handlelength=1.0,
            columnspacing=0.6,
            labelspacing=0.25
        )
    # Provide headroom so in-axes legend does not overlap data
    try:
        # IPC axis headroom
        # Estimate max from plotted data
        max_ipc = 0.0
        for v in variants:
            for krec in variant_data.get(v, []):
                if krec.get('ipc') is not None:
                    max_ipc = max(max_ipc, float(krec['ipc']))
        if max_ipc > 0:
            ymin, ymax = ax_ipc.get_ylim()
            ax_ipc.set_ylim(0, max(ymax, max_ipc * 1.2))
        # Fail axis headroom
        max_fail = 0
        for v in variants:
            for krec in variant_data.get(v, []):
                max_fail = max(max_fail, int(krec.get('r_total', 0)), int(krec.get('w_total', 0)))
        if max_fail > 0:
            ymin, ymax = ax_fail.get_ylim()
            ax_fail.set_ylim(0, max(ymax, max_fail * 1.2))
    except Exception:
        pass
    # Adjust top so suptitle has space above axes
    fig.subplots_adjust(top=0.9)
    ax_ipc.grid(axis='y', linestyle=':', alpha=0.4)
    ax_fail.grid(axis='y', linestyle=':', alpha=0.15)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'{benchmark}.png')
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    print(f'[INFO] Wrote {out_path}')

def discover_rodinia_benchmarks(sim_root: str) -> List[str]:
    out = []
    if not os.path.isdir(sim_root):
        return out
    for entry in os.listdir(sim_root):
        p = os.path.join(sim_root, entry)
        if os.path.isdir(p) and 'rodinia-2.0-ft' in entry:
            out.append(entry)
    return sorted(out)

def resolve_default_sim_root() -> str:
    env_root = os.getenv('ACCELSIM_ROOT')
    if not env_root:
        return ''
    candidate = os.path.abspath(os.path.join(env_root, '..', 'sim_run_12.1'))
    return candidate if os.path.isdir(candidate) else ''

def main():
    ap = argparse.ArgumentParser(description='Plot per-benchmark kernel IPC & fail stats comparing variants.')
    ap.add_argument('--sim-root', help='Path to sim_run_<cuda_ver> directory (defaults to $ACCELSIM_ROOT/../sim_run_12.1)')
    ap.add_argument('--benchmarks', nargs='*', help='Benchmark names (omit to auto-discover Rodinia benchmarks)')
    ap.add_argument('--variants', nargs='+', required=True, help='Variant tags to compare (e.g. regress-default-config regress-mshr-entries-32-again)')
    ap.add_argument('--output-dir', required=True, help='Directory for output plots')
    args = ap.parse_args()

    sim_root_raw = args.sim_root if args.sim_root else resolve_default_sim_root()
    # Expand environment variables and user home in provided paths
    sim_root = os.path.expanduser(os.path.expandvars(sim_root_raw)) if sim_root_raw else ''
    if not sim_root:
        print('[ERROR] sim-root not provided and default could not be resolved; set --sim-root or ACCELSIM_ROOT.')
        return
    benches = args.benchmarks if args.benchmarks else discover_rodinia_benchmarks(sim_root)
    if not benches:
        print('[WARN] No benchmarks discovered; exiting')
        return
    print(f'[INFO] Benchmarks to plot: {", ".join(benches)}')
    # Expand output directory too
    out_dir = os.path.expanduser(os.path.expandvars(args.output_dir))
    for b in benches:
        vdata = collect_benchmark(sim_root, b, args.variants)
        plot_benchmark(b, vdata, args.variants, out_dir)

if __name__ == '__main__':
        # Lightweight help trigger before argparse for convenience
        if len(sys.argv)==2 and sys.argv[1] in ('help','--help','-h'):
                print("""
plot_benchmark_fail_stats.py HELP

Mandatory:
    --variants <variant1> <variant2> [variant3 ...]
        Variant tags (directory names under QV100-SASS) to compare.

Optional:
    --sim-root <path>
        Path to sim_run_<cuda_ver> root. If omitted uses $ACCELSIM_ROOT/../sim_run_12.1
    --benchmarks <b1> <b2> ...
        Explicit benchmark names. If omitted auto-discovers rodinia-2.0-ft benchmarks.
    --output-dir <path>
        Directory for PNG output (required).

Examples:
    python perf_study/plot/plot_benchmark_fail_stats.py \
        --variants regress-default-config regress-mshr-entries-32-again \
        --output-dir perf_study/plot

    python perf_study/plot/plot_benchmark_fail_stats.py \
        --sim-root /abs/path/sim_run_12.1 \
        --benchmarks backprop-rodinia-2.0-ft bfs-rodinia-2.0-ft \
        --variants regress-default-config regress-mshr-entries-32-again \
        --output-dir perf_study/plot

Notes:
    - Dual y-axes: left=IPC, right=fail counts (read/write stacked).
    - If fail stats only at file end, same totals applied to all kernels.
    - Newest .o file per variant directory is chosen.
""")
                sys.exit(0)
        if len(sys.argv)==1:
                print(__doc__)
                sys.exit(0)
        main()
