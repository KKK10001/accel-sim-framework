#!/usr/bin/env python3
"""
plot-benchmark-fail-stats-per-item-plot.py

Each benchmark -> three separate PNG files:
  <bench>_ipc.png
  <bench>_l1d_fail_global_acc_r.png
  <bench>_l1d_fail_global_acc_w.png
Variants adjacent per kernel.

example usage:
# --geomean-target indicates which variant is the "tuned" one
# --geomean-metrics specifies the concerned metrics

python plot-benchmark-mshr-slots-occupancy.py \
    --sim-root "$ACCELSIM_ROOT/../sim_run_12.1" \
    --variants regress_disable_all_mshr \
        regress_en_all_mshr_l2_mshr_ent_192_slots_4 \
    --geomean-summary \
    --geomean-target regress_disable_all_mshr \
        regress_en_all_mshr_l2_mshr_ent_192_slots_4 \
    --geomean-metrics ipc global_acc_r global_acc_w \
    --export-l2-csv --export-l2-xlsx
"""
import argparse, copy, importlib, math, os, re, sys
import csv
from collections import defaultdict, OrderedDict
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional, Tuple
from matplotlib.patches import Patch

GPU_IPC_RE=re.compile(r"gpu_ipc\s*=\s*([0-9]+\.?[0-9]*)")
TOTAL_R_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\s*=\s*([0-9]+)")
TOTAL_W_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\s*=\s*([0-9]+)")
CAUSE_R_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\[(.+?)\]\s*=\s*([0-9]+)")
CAUSE_W_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\[(.+?)\]\s*=\s*([0-9]+)")
L2_MSHR_SLOT_ENTRY_RE=re.compile(r"L2_mshr_slots_occupancy\[sub:(\d+)\]\s*=\s*([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?\d+)?)")

def pick_latest(d):
    pat=re.compile(r".*\.o(\d+)?$")
    if not os.path.isdir(d): return ''
    c=[os.path.join(d,f) for f in os.listdir(d) if pat.match(f)]
    if not c: return ''
    c.sort(key=lambda p: os.path.getmtime(p), reverse=True); return c[0]

def parse(of):
    try: lines=open(of).read().splitlines()
    except: return []
    out=[]; cur=None; rT=0; wT=0; rR={}; wR={}
    def commit():
        if cur is not None:
            cur['r_total']=rT; cur['w_total']=wT; cur['r_reasons']=dict(rR); cur['w_reasons']=dict(wR); out.append(cur)
    for ln in lines:
        m=GPU_IPC_RE.search(ln)
        if m: commit(); cur={'ipc':float(m.group(1))}; continue
        m=TOTAL_R_RE.search(ln); m and (rT:=int(m.group(1)))
        m=TOTAL_W_RE.search(ln); m and (wT:=int(m.group(1)))
        m=CAUSE_R_RE.search(ln); m and (rR.__setitem__(m.group(1),int(m.group(2))))
        m=CAUSE_W_RE.search(ln); m and (wR.__setitem__(m.group(1),int(m.group(2))))
        m=L2_MSHR_SLOT_ENTRY_RE.search(ln)
        if m:
            if cur is None:
                cur={'ipc': None}
            occ=cur.setdefault('l2_mshr_slots_occupancy',{})
            try:
                occ[int(m.group(1))]=float(m.group(2))
            except ValueError:
                pass
            continue
    commit()
    if not out and (rT or wT): out=[{'ipc':None,'r_total':rT,'w_total':wT,'r_reasons':dict(rR),'w_reasons':dict(wR)}]
    return out

def collect(root,bench,variants)->Dict[str,List[Dict]]:
    res={}; bdir=os.path.join(root,bench)
    if not os.path.isdir(bdir): return res
    for sub in os.listdir(bdir):
        ap=os.path.join(bdir,sub,'QV100-SASS')
        if not os.path.isdir(ap): continue
        for v in variants:
            vdir=os.path.join(ap,v); of=pick_latest(vdir)
            if not of: continue
            res[v]=parse(of)
    return res

def ensure(data):
    if not data: return 0
    mc=max(len(l) for l in data.values())
    for v,l in data.items():
        if len(l)<mc and l:
            for _ in range(mc-len(l)):
                l.append(copy.deepcopy(l[-1]))
    return mc

def norm_variant(tag:str)->str:
    if tag.startswith('regress-'): tag=tag[len('regress-'):]
    elif tag.startswith('regress_'): tag=tag[len('regress_'):]
    if tag.endswith('-again'): tag=tag[:-len('-again')]
    # Treat any of the default-config aliases as the base configuration.
    if tag == 'disable_all_mshr': return 'base-config'
    if tag.startswith('disable_all_mshr'): return 'base-config'
    return tag


def short_variant_label(tag: str) -> str:
    norm = norm_variant(tag)
    replacements = [
        ('en_all_mshr_', ''),
        ('l2_mshr_ent_', 'l2_'),
        ('_slots_', '_slots'),
        ('slots_', 'slots'),
    ]
    for old, new in replacements:
        norm = norm.replace(old, new)
    norm = norm.replace('_', '-')
    return norm or tag


def strip_benchmark_suffix(bench: str) -> str:
    suffix = '-rodinia-2.0-ft'
    if bench.endswith(suffix):
        return bench[:-len(suffix)]
    return bench


def format_mosaic_csv_label(bench: str, variant: str) -> str:
    bench_label = strip_benchmark_suffix(bench)
    variant_label = short_variant_label(variant)
    if variant_label == 'l2-192-slots4':
        return bench_label
    return f'{bench_label}:{variant_label}'

def identify_base_and_tuned(variants:List[str])->tuple:
    base=None; tuned=None
    for v in variants:
        nv=norm_variant(v)
        if nv=='base-config' and base is None:
            base=v
        if 'mshr-entries-32' in v or 'mshr-entries-32' in nv:
            tuned=v
    return base, tuned


def normalize_cause_label(cause: str) -> str:
    if not cause:
        return cause
    if '][' in cause:
        return cause.split('][', 1)[0]
    return cause


def sanitize_label_for_path(label: str) -> str:
    cleaned=re.sub(r'[^0-9A-Za-z._-]+', '_', label)
    cleaned=cleaned.strip('_')
    return cleaned or 'target'


def aggregate_variant_fail_data(records: List[Dict]) -> Tuple[int, OrderedDict]:
    """Aggregate fail causes across all kernels for a single variant."""
    cause_totals: defaultdict = defaultdict(int)
    total_fails = 0
    for rec in records:
        for reason_key in ('r_reasons', 'w_reasons'):
            reasons = rec.get(reason_key) or {}
            for cause, count in reasons.items():
                normalized_cause = normalize_cause_label(cause)
                try:
                    amount = int(count)
                except (TypeError, ValueError):
                    continue
                if amount <= 0:
                    continue
                cause_totals[normalized_cause] += amount
                total_fails += amount
    ordered = OrderedDict()
    for cause, value in sorted(cause_totals.items(), key=lambda item: (-item[1], item[0])):
        ordered[cause] = value
    return total_fails, ordered


def aggregate_l2_mshr_slots(records: List[Dict]) -> Dict[str, Dict[int, float]]:
    per_kernel: defaultdict = defaultdict(lambda: defaultdict(list))
    for idx, rec in enumerate(records):
        occ_map = rec.get('l2_mshr_slots_occupancy') or {}
        kernel_key=f'kernel_{idx:03d}'
        for sub_idx, value in occ_map.items():
            try:
                sub_key=int(sub_idx)
                occ_val=float(value)
            except (TypeError, ValueError):
                continue
            per_kernel[kernel_key][sub_key].append(occ_val)
    averaged: Dict[str, Dict[int, float]]={}
    for kernel_key, sub_map in per_kernel.items():
        averaged[kernel_key]={sub_idx: float(np.mean(vals)) for sub_idx, vals in sub_map.items() if vals}
    if not averaged:
        return {}
    merged: Dict[int, list]=defaultdict(list)
    for sub_map in averaged.values():
        for sub_idx, val in sub_map.items():
            merged[sub_idx].append(val)
    averaged['__total__']={sub_idx: float(np.mean(vals)) for sub_idx, vals in merged.items() if vals}
    return averaged


def write_l2_mshr_slots_tables(out_dir: str,
                               bench: str,
                               ordered_subs: List[int],
                               present_variants: List[str],
                               aggregated: Dict[str, Dict[int, float]],
                               export_csv: bool,
                               export_xlsx: bool) -> Tuple[List[str], List[List[Optional[float]]]]:
    header=['l2_sub']+[norm_variant(v) for v in present_variants]
    rows: List[List[Optional[float]]] = []
    for sub in ordered_subs:
        row=[sub]
        for variant in present_variants:
            row.append(aggregated.get(variant, {}).get(sub))
        rows.append(row)
    if not (export_csv or export_xlsx):
        return header, rows
    if export_csv:
        csv_path=os.path.join(out_dir,f'{bench}_l2_mshr_slots_occupancy.csv')
        with open(csv_path,'w',newline='') as fh:
            writer=csv.writer(fh)
            writer.writerow(header)
            for row in rows:
                formatted=[row[0]]
                formatted.extend(f'{val:.6f}' if isinstance(val,(int,float)) else '' for val in row[1:])
                writer.writerow(formatted)
        print(f'[INFO] wrote L2 MSHR occupancy CSV to {csv_path}')
    if export_xlsx:
        spec=importlib.util.find_spec('openpyxl')
        if spec is None:
            print('[WARN] openpyxl not available; skip L2 MSHR occupancy XLSX export')
        else:
            openpyxl=importlib.import_module('openpyxl')
            wb=openpyxl.Workbook()
            ws=wb.active
            ws.title='L2_MSHR_Occupancy'
            ws.append(header)
            for row in rows:
                ws.append([row[0]]+row[1:])
            xlsx_path=os.path.join(out_dir,f'{bench}_l2_mshr_slots_occupancy.xlsx')
            wb.save(xlsx_path)
            print(f'[INFO] wrote L2 MSHR occupancy XLSX to {xlsx_path}')
    return header, rows


def render_fail_cause_mosaic(aggregated_data: Dict[str, Dict[str, Dict]],
                             variants: List[str],
                             output_dir: str) -> None:
    if not aggregated_data:
        print('[WARN] fail cause mosaic: no aggregated data to render')
        return

    benches = sorted(aggregated_data.keys())
    if not benches:
        print('[WARN] fail cause mosaic: no benchmarks available')
        return

    cause_totals_all: defaultdict = defaultdict(int)
    for bench_data in aggregated_data.values():
        for variant_data in bench_data.values():
            for cause, value in variant_data.get('cause_totals', {}).items():
                cause_totals_all[cause] += value

    if not cause_totals_all:
        print('[WARN] fail cause mosaic: no fail causes with data')
        return

    hatch_patterns=['////', '\\\\', 'xxxx', '++++', '....', '****', 'ooo', 'OO', '|||']
    cause_hatches={cause: hatch_patterns[idx % len(hatch_patterns)] for idx, (cause, _) in enumerate(sorted(cause_totals_all.items(), key=lambda item: (-item[1], item[0])))}

    cmap=plt.get_cmap('tab20')
    variant_colors={variant: cmap(idx % cmap.N) for idx, variant in enumerate(variants)}

    columns=min(5, max(1, len(benches)))
    rows=math.ceil(len(benches)/columns)
    fig, axes=plt.subplots(rows, columns, figsize=(columns*4.2, rows*3.2))
    if rows==1 and columns==1:
        axes_flat=[axes]
    else:
        axes_flat=list(np.array(axes).reshape(-1))

    bar_width=0.6
    for ax_idx, ax in enumerate(axes_flat):
        if ax_idx >= len(benches):
            ax.axis('off')
            continue
        bench=benches[ax_idx]
        bench_data=aggregated_data.get(bench, {})
        x_positions=np.arange(len(variants))
        for vidx, variant in enumerate(variants):
            variant_entry=bench_data.get(variant, {})
            total=variant_entry.get('total_fails', 0) or 0
            cause_map=variant_entry.get('cause_totals', OrderedDict())
            x_val=x_positions[vidx]
            bottom=0.0
            if total>0:
                for cause, value in cause_map.items():
                    if value<=0:
                        continue
                    ax.bar(
                        x_val,
                        value,
                        width=bar_width,
                        bottom=bottom,
                        facecolor=variant_colors[variant],
                        edgecolor='black',
                        linewidth=0.8,
                        hatch=cause_hatches.get(cause,'/'),
                    )
                    bottom+=value

        ax.set_xticks(x_positions)
        ax.set_xticklabels(['']*len(variants))
        if len(variants) > 0:
            ax.set_xlim(-0.6, len(variants) - 0.4)
        ax.text(
            0.5,
            1.03,
            bench,
            transform=ax.transAxes,
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

        bench_cause_totals=defaultdict(int)
        for variant_entry in bench_data.values():
            for cause, value in variant_entry.get('cause_totals', {}).items():
                bench_cause_totals[cause]+=value
        bench_cause_handles=[
            Patch(facecolor='#ffffff', edgecolor='black', hatch=cause_hatches.get(cause,'/'), label=cause, linewidth=0.8)
            for cause in sorted(bench_cause_totals.keys(), key=lambda c: (-bench_cause_totals[c], c))
        ]
        if bench_cause_handles:
            ax.legend(
                bench_cause_handles,
                [patch.get_label() for patch in bench_cause_handles],
                loc='upper right',
                fontsize='x-small',
                frameon=False,
                borderaxespad=0.2,
                handlelength=1.2,
            )
        bench_total_max=max((entry.get('total_fails', 0) or 0) for entry in bench_data.values())
        if bench_total_max<=0:
            ax.set_ylim(0, 1)
        else:
            y_pad=max(bench_total_max*0.1, 1.0)
            ax.set_ylim(0, bench_total_max+y_pad)

    legend_rows = 1 if len(variants) <= 4 else 2
    legend_height = 0.06 * legend_rows + 0.02
    legend_pad = 0.02
    extra_margin = 0.08 + 0.015 * (legend_rows - 1)
    subplot_top = max(0.55, 1.0 - legend_height - legend_pad - extra_margin)
    fig.subplots_adjust(left=0.05, right=0.99, top=subplot_top, wspace=0.2, hspace=0.32)
    subplot_params = fig.subplotpars
    legend_left = subplot_params.left
    legend_right = subplot_params.right
    legend_width = max(0.1, legend_right - legend_left)

    variant_handles=[
        Patch(facecolor=variant_colors[variant], edgecolor='black', label=norm_variant(variant), linewidth=0.8)
        for variant in variants
    ]
    legend_cols = max(1, math.ceil(len(variants) / legend_rows))
    legend_y = subplot_top + 0.005
    legend_top = legend_y + legend_height
    if legend_top > 0.96:
        legend_y = max(0.6, 0.96 - legend_height)
    legend_bbox = (legend_left, legend_y, legend_width, legend_height)
    fig.legend(
        variant_handles,
        [norm_variant(v) for v in variants],
        loc='upper left',
        bbox_to_anchor=legend_bbox,
        ncol=legend_cols,
        frameon=False,
        columnspacing=0.9,
        handlelength=1.4,
        borderaxespad=0.0,
        mode='expand'
    )
    title_y = min(0.99, legend_y + legend_height + 0.06)
    fig.suptitle('Per-benchmark fail cause breakdown (TOTAL fails)', fontsize=15, y=title_y)
    mosaic_path=os.path.join(output_dir, 'fail_cause_benchmark_mosaic.png')
    fig.savefig(mosaic_path, dpi=180)
    plt.close(fig)
    print(f'[INFO] wrote fail cause mosaic to {mosaic_path}')


def format_fail_delta(feature_total: float, base_total: Optional[float]) -> Optional[str]:
    if base_total is None:
        return None
    if base_total == 0:
        if feature_total == 0:
            return '(0.00%)'
        return '(+∞%)'
    if feature_total == 0:
        return '(-100%)'
    delta = (feature_total - base_total) / base_total * 100.0
    return f"({delta:+.2f}%)"


def find_variant_by_normalized(variants: List[str], normalized_tag: str) -> Optional[str]:
    for variant in variants:
        if norm_variant(variant) == normalized_tag:
            return variant
    return None


METRIC_VALUE_KEYS: Dict[str, str] = {
    'ipc': 'ipc',
    'global_acc_r': 'r_total',
    'global_acc_w': 'w_total',
}

METRIC_TITLES: Dict[str, str] = {
    'ipc': 'IPC',
    'global_acc_r': 'GLOBAL_ACC_R fails',
    'global_acc_w': 'GLOBAL_ACC_W fails',
}

METRIC_AXIS_LABELS: Dict[str, str] = {
    'ipc': 'IPC (geomean)',
    'global_acc_r': 'Fail counts (geomean)',
    'global_acc_w': 'Fail counts (geomean)',
}


def geometric_mean_from_records(records: List[Dict], value_key: str) -> Optional[float]:
    if not records:
        return None
    values: List[float] = []
    for rec in records:
        val = rec.get(value_key)
        if val is None:
            continue
        try:
            fval = float(val)
        except (TypeError, ValueError):
            continue
        if math.isnan(fval):
            continue
        values.append(max(fval, 0.0))
    if not values:
        return None
    positive_values = [v for v in values if v > 0.0]
    if len(positive_values) == len(values):
        log_sum = sum(math.log(v) for v in positive_values)
        return math.exp(log_sum / len(positive_values))
    if not positive_values:
        return 0.0
    log_sum = sum(math.log(v + 1.0) for v in values)
    return math.exp(log_sum / len(values)) - 1.0


def render_geomean_summary(metric: str,
                           results: List[Tuple[str, float, float]],
                           output_dir: str,
                           base_label: str,
                           target_label: str) -> None:
    filtered = [(bench, base, target) for bench, base, target in results if base is not None and target is not None]
    if not filtered:
        print(f"[WARN] geomean summary: no complete data for metric {metric}")
        return

    summary_dir = os.path.join(output_dir, 'geomean', sanitize_label_for_path(target_label))
    os.makedirs(summary_dir, exist_ok=True)
    per_benchmark_paths: List[str] = []
    width = 0.35
    for bench, base_val, target_val in filtered:
        fig, ax = plt.subplots(figsize=(3.6, 3.2))
        positions = [-width / 2, width / 2]
        ax.bar(positions[0], base_val, width=width, color='#1f77b4', label=base_label)
        ax.bar(positions[1], target_val, width=width, color='#d62728', label=target_label)
        ax.set_xticks(positions)
        ax.set_xticklabels(['', ''])
        ax.set_ylabel(METRIC_AXIS_LABELS.get(metric, metric))
        ax.set_title(bench, fontsize=10)
        ax.grid(axis='y', linestyle=':', alpha=0.3)
        offset = max(abs(target_val) * 0.06, 0.5)
        delta_label = format_fail_delta(target_val, base_val)
        delta_font_size = 10
        if delta_label:
            y_pos = target_val + offset if target_val >= 0 else offset
            ax.text(positions[1], y_pos, delta_label, ha='center', va='bottom', fontsize=delta_font_size)
        max_val = max(base_val, target_val)
        if max_val == 0.0:
            upper = max(1.0, offset * 2 if delta_label else 1.0)
        else:
            upper_padding = max(max_val * 0.2, offset * 2 if delta_label else max_val * 0.12)
            upper = max_val + upper_padding
        ax.set_ylim(0.0, upper)
        fig.tight_layout()
        out_path = os.path.join(summary_dir, f'{bench}_{metric}_geomean.png')
        fig.savefig(out_path, dpi=160)
        plt.close(fig)
        per_benchmark_paths.append(out_path)
        print(f'[INFO] wrote per-benchmark geomean chart {out_path}')

    columns = 5
    rows = math.ceil(len(per_benchmark_paths) / columns)
    mosaic_width = columns * 3.6
    mosaic_height = rows * 3.2
    mosaic_fig, mosaic_axes = plt.subplots(rows, columns, figsize=(mosaic_width, mosaic_height))
    if rows == 1:
        mosaic_axes = [mosaic_axes]
    axes_flat = [ax for row_axes in mosaic_axes for ax in (row_axes if isinstance(row_axes, (list, tuple, np.ndarray)) else [row_axes])]

    for ax, path in zip(axes_flat, per_benchmark_paths):
        img = plt.imread(path)
        ax.imshow(img)
        ax.axis('off')
    for ax in axes_flat[len(per_benchmark_paths):]:
        ax.axis('off')

    legend_handles = [
        Patch(facecolor='#1f77b4', label=base_label),
        Patch(facecolor='#d62728', label=target_label),
    ]
    mosaic_fig.legend(
        legend_handles,
        [base_label, target_label],
        loc='upper left',
        bbox_to_anchor=(0.01, 0.99),
        ncol=2,
        frameon=False,
        columnspacing=1.5,
        handlelength=1.5,
    )
    mosaic_fig.suptitle(
        f'Geometric Mean Comparison - {METRIC_TITLES.get(metric, metric)}',
        fontsize=16,
        y=0.965
    )
    mosaic_fig.tight_layout(rect=[0, 0, 1, 0.9])
    mosaic_path = os.path.join(summary_dir, f'geomean_{metric}_mosaic.png')
    mosaic_fig.savefig(mosaic_path, dpi=160)
    plt.close(mosaic_fig)
    print(f'[INFO] wrote geomean mosaic to {mosaic_path}')

def plot_ipc(bench,data,variants,kc,out_root_dir):
    # ensure subfolder ipc
    out_dir=os.path.join(out_root_dir,'ipc'); os.makedirs(out_dir,exist_ok=True)
    xs=list(range(kc)); fig,ax=plt.subplots(figsize=(max(6,kc*0.9),3))
    span=0.8; vcnt=len(variants); vspan=span/vcnt; gap=vspan*0.15; width=vspan-gap
    cmap=plt.get_cmap('tab10')
    colors={variant: cmap(idx % cmap.N) for idx, variant in enumerate(variants)}
    base_tag, tuned_tag = identify_base_and_tuned(variants)
    tuned_positions=[]; tuned_values=[]; base_values=[]
    for ki in range(kc):
        for vi,v in enumerate(variants):
            recs=data.get(v,[]); 
            if ki>=len(recs): continue
            rec=recs[ki];
            if rec.get('ipc') is None: continue
            x=xs[ki]-span/2+vi*vspan+gap/2+width/2
            ax.bar(x,rec['ipc'],width=width,color=colors[v])
            if v==tuned_tag:
                tuned_positions.append(x)
                tuned_values.append(rec['ipc'])
                if base_tag and ki < len(data.get(base_tag,[])):
                    base_values.append(data[base_tag][ki].get('ipc'))
                else:
                    base_values.append(None)
    if tuned_tag and base_tag and tuned_positions:
        for x,ipc_tuned,ipc_base in zip(tuned_positions,tuned_values,base_values):
            if ipc_base and ipc_base>0 and ipc_tuned is not None:
                gain=(ipc_tuned-ipc_base)/ipc_base*100.0
                ax.text(x, ipc_tuned*1.03, f"{gain:+.1f}%", ha='center', va='bottom', fontsize=7)
    ax.set_xticks(xs); ax.set_xticklabels([f'k{ki+1}' for ki in xs],rotation=20)
    ax.set_ylabel('IPC'); ax.set_title(f'{bench} IPC')
    # legend
    handles=[Patch(facecolor=colors.get(v,'#999')) for v in variants[:2]]
    labels=[norm_variant(v) for v in variants[:2]]
    ax.legend(handles,labels,fontsize='x-small')
    fig.tight_layout(); fig.savefig(os.path.join(out_dir,f'{bench}_ipc.png'),dpi=150); plt.close(fig)

def plot_fail(bench,data,variants,kc,out_root_dir,kind:str):
    sub_map={'r':'global_acc_r','w':'global_acc_w'}
    sub_folder=sub_map.get(kind,'fails')
    out_dir=os.path.join(out_root_dir,sub_folder); os.makedirs(out_dir,exist_ok=True)
    xs=list(range(kc)); fig,ax=plt.subplots(figsize=(max(6,kc*0.9),3))
    span=0.8; vcnt=len(variants); vspan=span/vcnt; gap=vspan*0.15; width=vspan-gap
    cmap=plt.get_cmap('tab10')
    colors={variant: cmap(idx % cmap.N) for idx, variant in enumerate(variants)}
    # collect reasons
    all_causes=set()
    for v in variants:
        for rec in data.get(v,[]): all_causes.update(rec[f'{kind}_reasons'].keys())
    cycle=['////','\\\\','xxxx','++++','....','****','ooo','OO']
    h={r:cycle[i%len(cycle)] for i,r in enumerate(sorted(all_causes))}
    cause_totals={cause:0 for cause in all_causes}
    base_tag, tuned_tag = identify_base_and_tuned(variants)
    base_records = data.get(base_tag, []) if base_tag else []
    annotations: List[Tuple[float, float, str, bool]] = []
    max_height = 0.0
    for ki in range(kc):
        base_total = None
        if base_records and ki < len(base_records):
            base_total = float(base_records[ki].get(f'{kind}_total', 0) or 0)
            max_height = max(max_height, base_total)
        for vi,v in enumerate(variants):
            recs=data.get(v,[]);
            if ki>=len(recs): continue
            rec=recs[ki]
            total=float(rec.get(f'{kind}_total',0) or 0)
            x=xs[ki]-span/2+vi*vspan+gap/2+width/2
            stacked_height=0.0
            if total>0:
                for rea,val in sorted(rec[f'{kind}_reasons'].items()):
                    if val==0: continue
                    ax.bar(x,val,width=width,bottom=stacked_height,color=colors[v],hatch=h.get(rea,'/'),edgecolor='black')
                    cause_totals[rea]=cause_totals.get(rea,0)+val
                    stacked_height+=val
                max_height = max(max_height, stacked_height)
            if v == tuned_tag:
                label = format_fail_delta(total, base_total)
                if label:
                    annotations.append((x, stacked_height, label, total > 0))
    ax.set_xticks(xs); ax.set_xticklabels([f'k{ki+1}' for ki in xs],rotation=20)
    ax.set_ylabel('Fail counts'); title_map={'r':'GLOBAL_ACC_R','w':'GLOBAL_ACC_W'}
    ax.set_title(f'{bench} {title_map[kind]} fails')
    variant_handles=[Patch(facecolor=colors.get(v,'#999'), edgecolor='black') for v in variants]
    variant_labels=[norm_variant(v) for v in variants]
    cause_handles=[
        Patch(
            facecolor='#e0e0e0',
            edgecolor='black',
            hatch=h.get(cause,'/'),
            linewidth=0.6
        )
        for cause,val in sorted(cause_totals.items()) if val>0
    ]
    cause_labels=[cause for cause,val in sorted(cause_totals.items()) if val>0]
    legend_anchor_x=1.02
    if variant_handles:
        variant_legend=ax.legend(
            variant_handles,
            variant_labels,
            title='Variants',
            fontsize='x-small',
            title_fontsize='small',
            loc='upper left',
            bbox_to_anchor=(legend_anchor_x, 1.0),
            borderaxespad=0.0
        )
        ax.add_artist(variant_legend)
    if cause_handles:
        ax.legend(
            cause_handles,
            cause_labels,
            title='Fail causes',
            fontsize='x-small',
            title_fontsize='small',
            loc='upper left',
            bbox_to_anchor=(legend_anchor_x, 0.62),
            borderaxespad=0.0
        )

    if annotations:
        offset = max(max_height * 0.04, 1.0) if max_height > 0 else 1.0
        for x_pos, height, text, has_bar in annotations:
            y_pos = height + offset if has_bar else offset
            ax.text(x_pos, y_pos, text, ha='center', va='bottom', fontsize=7, color='black')
        current_ylim = ax.get_ylim()
        upper_needed = max_height + offset * 4
        if current_ylim[1] < upper_needed:
            ax.set_ylim(current_ylim[0], upper_needed)
    fig.tight_layout(rect=[0, 0, 0.86, 1]); fname=f'{bench}_l1d_fail_global_acc_{"r" if kind=="r" else "w"}.png'
    fig.savefig(os.path.join(out_dir,fname),dpi=150); plt.close(fig)


def plot_l2_mshr_slots_occupancy(bench, data, variants, out_root_dir, export_csv: bool, export_xlsx: bool):
    out_dir=os.path.join(out_root_dir,'l2_mshr_slots_occupancy'); os.makedirs(out_dir,exist_ok=True)
    aggregated={}; sub_indices=set()
    for variant in variants:
        variant_records=data.get(variant, [])
        occ_map=aggregate_l2_mshr_slots(variant_records)
        total_map=occ_map.get('__total__') if occ_map else None
        if total_map:
            aggregated[variant]=total_map
            sub_indices.update(total_map.keys())
    if not aggregated:
        print(f'[WARN] no L2 MSHR slots occupancy data for {bench}')
        return
    ordered_subs=sorted(sub_indices)
    present_variants=[v for v in variants if v in aggregated]
    if not present_variants:
        print(f'[WARN] variants lack L2 MSHR data for {bench}')
        return
    xs=np.arange(len(ordered_subs))
    width=0.8/max(1,len(present_variants))
    cmap=plt.get_cmap('tab10')
    colors={variant: cmap(idx % cmap.N) for idx, variant in enumerate(variants)}
    height_cache={variant:[aggregated[variant].get(sub,0.0) for sub in ordered_subs] for variant in present_variants}
    max_height=max((max(vals) for vals in height_cache.values() if vals), default=0.0)
    label_offset=max(max_height*0.03,0.02) if max_height>0 else 0.05
    fig,ax=plt.subplots(figsize=(max(6,len(ordered_subs)*1.0),3.2))
    for idx,variant in enumerate(present_variants):
        offsets=xs-0.4+width/2+idx*width
        heights=height_cache[variant]
        ax.bar(offsets,heights,width=width,color=colors.get(variant,'#999'),edgecolor='black',label=norm_variant(variant))
        for x_pos,height in zip(offsets,heights):
            if height<=0: continue
            ax.text(x_pos,height+label_offset,f'{height:.3f}',ha='center',va='bottom',fontsize=7)
    ax.set_xticks(xs)
    ax.set_xticklabels([f'sub {sub}' for sub in ordered_subs],rotation=20)
    upper=max_height+max(label_offset*2,0.1) if max_height>0 else 1.0
    ax.set_ylim(0,upper)
    ax.set_ylabel('Average L2 MSHR slots occupancy')
    ax.set_title(f'{bench} L2 MSHR slots occupancy')
    ax.grid(axis='y',linestyle=':',alpha=0.3)
    ax.legend(fontsize='x-small',loc='upper right',frameon=False)
    fig.tight_layout(rect=[0,0,0.96,1])
    fig.savefig(os.path.join(out_dir,f'{bench}_l2_mshr_slots_occupancy.png'),dpi=150)
    plt.close(fig)
    return write_l2_mshr_slots_tables(out_dir, bench, ordered_subs, present_variants, aggregated, export_csv, export_xlsx)


def render_l2_mshr_slots_mosaic(out_root_dir: str,
                                benchmarks: List[str],
                                per_bench_tables: Dict[str, Tuple[List[str], List[List[Optional[float]]]]],
                                export_csv: bool) -> None:
    src_dir=os.path.join(out_root_dir,'l2_mshr_slots_occupancy')
    if not os.path.isdir(src_dir):
        print(f'[WARN] l2 MSHR mosaic: source directory missing: {src_dir}')
        return
    images=[]
    labels=[]
    bench_variant_order: List[Tuple[str, str]] = []
    bench_variant_seen: set = set()
    sub_value_map: Dict[object, Dict[Tuple[str, str], Optional[float]]] = defaultdict(dict)
    for bench in benchmarks:
        fname=f'{bench}_l2_mshr_slots_occupancy.png'
        path=os.path.join(src_dir,fname)
        if os.path.isfile(path):
            try:
                images.append(plt.imread(path))
                labels.append(bench)
                header_rows=per_bench_tables.get(bench)
                if header_rows:
                    header, rows=header_rows
                    variants = header[1:]
                    for variant in variants:
                        key=(bench, variant)
                        if key not in bench_variant_seen:
                            bench_variant_order.append(key)
                            bench_variant_seen.add(key)
                    for row in rows:
                        if not row:
                            continue
                        sub_key = row[0]
                        try:
                            sub_key = int(sub_key)
                        except (TypeError, ValueError):
                            pass
                        for variant, value in zip(variants, row[1:]):
                            col_key=(bench, variant)
                            if value is None:
                                continue
                            sub_value_map[sub_key][col_key]=value
            except Exception as err:
                print(f'[WARN] l2 MSHR mosaic: skip {path}: {err}')
    if not images:
        print('[WARN] l2 MSHR mosaic: no images to compose')
        return
    columns=2
    rows=5
    fig, axes=plt.subplots(rows, columns, figsize=(columns*4.2, rows*2.8), constrained_layout=False)
    axes_flat=[ax for row in axes for ax in (row if isinstance(row, (list, tuple, np.ndarray)) else [row])]
    for ax, img, label in zip(axes_flat, images, labels):
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(label, fontsize=10)
    for ax in axes_flat[len(images):]:
        ax.axis('off')
    fig.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.04, hspace=0.24, wspace=0.08)
    fig.suptitle('Per-benchmark L2 MSHR slots occupancy', fontsize=16, y=0.965)
    mosaic_path=os.path.join(src_dir,'l2_mshr_slots_occupancy_mosaic.png')
    fig.savefig(mosaic_path,dpi=160)
    plt.close(fig)
    print(f'[INFO] wrote L2 MSHR occupancy mosaic to {mosaic_path}')
    if export_csv and bench_variant_order and sub_value_map:
        csv_header=['l2_sub']+[format_mosaic_csv_label(bench, variant) for bench, variant in bench_variant_order]+['avg']
        csv_rows=[]
        for sub_idx in sorted(sub_value_map.keys(), key=lambda x: (isinstance(x, str), x)):
            row=[sub_idx]
            value_map=sub_value_map[sub_idx]
            per_row_values: List[float] = []
            for col_key in bench_variant_order:
                val=value_map.get(col_key)
                row.append(val)
                if isinstance(val,(int,float)):
                    per_row_values.append(val)
            row.append(sum(per_row_values)/len(per_row_values) if per_row_values else None)
            csv_rows.append(row)
        avg_row=['avg']
        for col_idx in range(1, len(csv_header)):
            values=[row[col_idx] for row in csv_rows if isinstance(row[col_idx], (int, float))]
            avg_row.append(sum(values)/len(values) if values else None)
        csv_rows.append(avg_row)
        mosaic_csv=os.path.join(src_dir,'l2_mshr_slots_occupancy_mosaic.csv')
        with open(mosaic_csv,'w',newline='') as fh:
            writer=csv.writer(fh)
            writer.writerow(csv_header)
            for row in csv_rows:
                formatted=[row[0]]
                formatted.extend(
                    f'{val:.6f}' if isinstance(val,(int,float)) else ''
                    for val in row[1:]
                )
                writer.writerow(formatted)
        print(f'[INFO] wrote L2 MSHR occupancy mosaic CSV to {mosaic_csv}')

def main():
    ap=argparse.ArgumentParser(description='Separate plots per benchmark (IPC, read fails, write fails).')
    ap.add_argument('--sim-root',help='Path to sim_run_<ver> (default $ACCELSIM_ROOT/../sim_run_12.1)')
    ap.add_argument('--benchmarks',nargs='*',help='Benchmarks (omit to auto-discover).')
    ap.add_argument('--variants',nargs='+',required=True,help='Variant tags.')
    ap.add_argument('--output-dir',help='Destination directory (default ./per-item-plot)')
    ap.add_argument('--geomean-summary', action='store_true', help='Also render geomean comparison plots across benchmarks.')
    ap.add_argument('--geomean-target', dest='geomean_targets', nargs='+', default=['mshr-entries-32'], help='Normalized names of the tuned variant(s) to compare against base-config (default: mshr-entries-32).')
    ap.add_argument('--geomean-metrics', nargs='*', default=['global_acc_r'], choices=['ipc','global_acc_r','global_acc_w'], help='Metric list for geomean summary (default: global_acc_r).')
    ap.add_argument('--export-l2-csv', action='store_true', help='Write L2 MSHR occupancy data to CSV alongside charts.')
    ap.add_argument('--export-l2-xlsx', action='store_true', help='Write L2 MSHR occupancy data to XLSX alongside charts (requires openpyxl).')
    args=ap.parse_args()
    env=os.getenv('ACCELSIM_ROOT'); root=os.path.expanduser(os.path.expandvars(args.sim_root)) if args.sim_root else (os.path.abspath(os.path.join(env,'..','sim_run_12.1')) if env else '')
    if not root: sys.exit('[ERROR] sim-root unresolved')
    benches=args.benchmarks if args.benchmarks else [d for d in os.listdir(root) if 'rodinia-2.0-ft' in d and os.path.isdir(os.path.join(root,d))]
    if not benches: sys.exit('[WARN] no benchmarks found')
    out_dir = args.output_dir or './per-item-plot'
    os.makedirs(out_dir,exist_ok=True)
    # create subfolders if not exist
    for sf in ['ipc','global_acc_r','global_acc_w','l2_mshr_slots_occupancy']:
        os.makedirs(os.path.join(out_dir,sf),exist_ok=True)

    base_variant = find_variant_by_normalized(args.variants, 'base-config')
    geomean_target_pairs: List[Tuple[str, str]] = []
    if args.geomean_summary:
        if base_variant is None:
            sys.exit('[ERROR] geomean summary requires default-config in --variants')
        seen_targets=set()
        missing_targets=[]
        for target in args.geomean_targets:
            if not target or not str(target).strip():
                continue
            normalized=norm_variant(target)
            if normalized in seen_targets:
                continue
            seen_targets.add(normalized)
            resolved=find_variant_by_normalized(args.variants, normalized)
            if resolved is None:
                missing_targets.append(target)
                continue
            geomean_target_pairs.append((normalized, resolved))
        if missing_targets:
            print(f"[WARN] geomean target(s) not present in --variants: {', '.join(missing_targets)}")
        if not geomean_target_pairs:
            print('[WARN] no valid geomean targets resolved; skipping geomean summary.')
            args.geomean_summary=False

    geomean_results: Dict[str, Dict[str, List[Tuple[str, float, float]]]] = {}
    if args.geomean_summary:
        geomean_results={label: {metric: [] for metric in args.geomean_metrics} for label, _ in geomean_target_pairs}
    aggregated_fail_summary: Dict[str, Dict[str, Dict[str, object]]] = {}
    per_bench_tables: Dict[str, Tuple[List[str], List[List[Optional[float]]]]] = {}

    for b in benches:
        data=collect(root,b,args.variants)
        raw_data={variant: list(records) for variant, records in data.items()}
        bench_summary: Dict[str, Dict[str, object]] = {}
        for variant in args.variants:
            variant_records=raw_data.get(variant, [])
            total_fails, cause_totals = aggregate_variant_fail_data(variant_records)
            bench_summary[variant]={
                'total_fails': total_fails,
                'cause_totals': cause_totals,
            }
        aggregated_fail_summary[b]=bench_summary
        if args.geomean_summary:
            base_records = raw_data.get(base_variant, [])
            for target_label, target_variant in geomean_target_pairs:
                target_records = raw_data.get(target_variant, [])
                if not (base_records and target_records):
                    print(f"[WARN] geomean summary: missing data for benchmark {b} (target: {target_label})")
                    continue
                for metric in args.geomean_metrics:
                    value_key = METRIC_VALUE_KEYS.get(metric)
                    if value_key is None:
                        continue
                    base_value = geometric_mean_from_records(base_records, value_key)
                    target_value = geometric_mean_from_records(target_records, value_key)
                    if base_value is None or target_value is None:
                        continue
                    geomean_results[target_label][metric].append((b, base_value, target_value))

        kc=ensure(data)
        table_header_rows=plot_l2_mshr_slots_occupancy(b,raw_data,args.variants,out_dir,args.export_l2_csv,args.export_l2_xlsx)
        per_bench_tables[b]=table_header_rows
        if kc==0:
            continue
        plot_ipc(b,data,args.variants,kc,out_dir)
        plot_fail(b,data,args.variants,kc,out_dir,'r')
        plot_fail(b,data,args.variants,kc,out_dir,'w')
        print(f'[INFO] wrote separate plots for {b} into {out_dir}/ipc, {out_dir}/global_acc_r, {out_dir}/global_acc_w, {out_dir}/l2_mshr_slots_occupancy')

    if args.geomean_summary and geomean_results:
        base_label = norm_variant(base_variant) if base_variant else 'base-config'
        for target_label, metric_map in geomean_results.items():
            for metric, results in metric_map.items():
                render_geomean_summary(metric, results, out_dir, base_label, target_label)

    render_fail_cause_mosaic(aggregated_fail_summary, args.variants, out_dir)
    render_l2_mshr_slots_mosaic(out_dir, benches, per_bench_tables, args.export_l2_csv)

if __name__=='__main__': main()
