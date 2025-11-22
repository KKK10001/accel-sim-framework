#!/usr/bin/env python3
"""
compute_perf_gain.py

Generates performance gain outputs comparing base vs tuned variant:
    - Text (legacy): perf_gain.txt
    - CSV: perf_gain.csv
    - Markdown: perf_gain.md (tables per benchmark + summary)

Metrics:
    IPC, GLOBAL_ACC_R fail count, GLOBAL_ACC_W fail count.

Base variant identified from tag 'default-config' (normalized to 'base-config').
Tuned variant identified by substring 'mshr-entries-32'.
Infinite percentage change (base == 0 and tuned > 0) rendered as 'inf'.

example useage:
python3 compute_perf_gain.py \
  --variants regress-default-config regress-mshr-entries-32-again \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx
"""
import argparse, os, re, sys, math
from copy import copy

GPU_IPC_RE = re.compile(r"gpu_ipc\s*=\s*([0-9]+\.?[0-9]*)")
TOTAL_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\s*=\s*([0-9]+)")
TOTAL_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\s*=\s*([0-9]+)")

def pick_latest_o_file(variant_dir: str) -> str:
    pat = re.compile(r".*\.o(\d+)?$")
    if not os.path.isdir(variant_dir): return ''
    files = [f for f in os.listdir(variant_dir) if pat.match(f)]
    if not files: return ''
    paths=[os.path.join(variant_dir,f) for f in files]
    paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return paths[0]

def parse_o_file(path: str):
    try:
        lines=open(path).read().splitlines()
    except Exception:
        return []
    kernels=[]; current=None
    r_total=0; w_total=0
    def commit():
        if current is not None:
            current['r_total']=r_total; current['w_total']=w_total; kernels.append(current)
    for line in lines:
        m=GPU_IPC_RE.search(line)
        if m:
            commit(); current={'ipc':float(m.group(1))}; continue
        m=TOTAL_R_RE.search(line); m and (r_total:=int(m.group(1)))
        m=TOTAL_W_RE.search(line); m and (w_total:=int(m.group(1)))
    commit()
    if not kernels and (r_total or w_total):
        kernels=[{'ipc':None,'r_total':r_total,'w_total':w_total}]
    return kernels

def discover(root:str):
    return sorted([d for d in os.listdir(root) if 'rodinia-2.0-ft' in d and os.path.isdir(os.path.join(root,d))])

def default_sim_root()->str:
    env=os.getenv('ACCELSIM_ROOT')
    if not env: return ''
    cand=os.path.abspath(os.path.join(env,'..','sim_run_12.1'))
    return cand if os.path.isdir(cand) else ''

def find_base_and_tuned(variants):
    base=None; tuned=None
    for v in variants:
        nv=v
        if nv.startswith('regress-'): nv=nv[len('regress-'):]
        if nv.endswith('-again'): nv=nv[:-len('-again')]
        if nv=='default-config': nv='base-config'
        if nv=='base-config' and base is None:
            base=v
        if 'mshr-entries-32' in v or 'mshr-entries-32' in nv:
            tuned=v
    return base, tuned

def normalize_variant_name(v: str) -> str:
    nv=v
    if nv.startswith('regress-'):
        nv=nv[len('regress-'):]
    if nv.endswith('-again'):
        nv=nv[:-len('-again')]
    if nv=='default-config':
        nv='base-config'
    return nv

def collect_variant(root, bench, variant):
    bdir=os.path.join(root, bench)
    if not os.path.isdir(bdir): return []
    # choose first args_sub that yields data
    for args_sub in os.listdir(bdir):
        ap=os.path.join(bdir,args_sub,'QV100-SASS',variant)
        of=pick_latest_o_file(ap)
        if of:
            return parse_o_file(of)
    return []

def pct_change(tuned, base):
    if base is None or base==0:
        if tuned is None or tuned==0: return 0.0
        return float('inf')
    return (tuned-base)/base*100.0


def geometric_mean_from_records(records, value_key):
    if not records:
        return None
    values=[]
    for rec in records:
        val=rec.get(value_key)
        if val is None:
            continue
        try:
            fval=float(val)
        except (TypeError, ValueError):
            continue
        if math.isnan(fval):
            continue
        values.append(max(fval, 0.0))
    if not values:
        return None
    positive_values=[v for v in values if v>0.0]
    if len(positive_values)==len(values):
        log_sum=sum(math.log(v) for v in positive_values)
        return math.exp(log_sum/len(positive_values))
    if not positive_values:
        return 0.0
    log_sum=sum(math.log(v+1.0) for v in values)
    return math.exp(log_sum/len(values))-1.0


def ratio_from_geomeans(base_val, tuned_val):
    if base_val is None or tuned_val is None:
        return None
    if base_val == 0.0:
        if tuned_val == 0.0:
            return 1.0
        return float('inf')
    return tuned_val / base_val


def ratio_to_pct(ratio):
    if ratio is None:
        return None
    if ratio==float('inf'):
        return float('inf')
    return (ratio-1.0)*100.0


def geometric_mean(values):
    cleaned=[]
    for val in values:
        if val is None:
            continue
        try:
            fval=float(val)
        except (TypeError, ValueError):
            continue
        if math.isnan(fval):
            continue
        cleaned.append(max(fval, 0.0))
    if not cleaned:
        return None
    positive=[v for v in cleaned if v>0.0]
    if len(positive)==len(cleaned):
        log_sum=sum(math.log(v) for v in positive)
        return math.exp(log_sum/len(positive))
    if not positive:
        return 0.0
    log_sum=sum(math.log(v+1.0) for v in cleaned)
    return math.exp(log_sum/len(cleaned))-1.0


METRIC_ORDER=['ipc','global_acc_r','global_acc_w']
METRIC_VALUE_KEYS={'ipc':'ipc','global_acc_r':'r_total','global_acc_w':'w_total'}
METRIC_LABELS={'ipc':'IPC','global_acc_r':'GLOBAL_ACC_R fails','global_acc_w':'GLOBAL_ACC_W fails'}


def format_value(value):
    if value is None:
        return 'NA'
    if value==float('inf'):
        return 'inf'
    if value==float('-inf'):
        return '-inf'
    return f"{value:.3f}"


def format_pct(value):
    if value is None:
        return 'NA'
    if value==float('inf'):
        return 'inf'
    return f"{value:.3f}"


def format_pct_signed(value):
    if value is None:
        return None
    if value==float('inf'):
        return '+inf'
    if value==float('-inf'):
        return '-inf'
    return f"{value:+.3f}"


def format_actual_with_pct(actual, pct, include_pct=True):
    actual_str=format_value(actual)
    if actual is None:
        return actual_str
    if not include_pct or pct is None:
        return actual_str
    pct_str=format_pct_signed(pct)
    if pct_str is None:
        return actual_str
    return f"{actual_str} ({pct_str}%)"


def pct_to_float(value):
    if value is None:
        return 0.0
    if value==float('inf'):
        return float('inf')
    return float(value)


def parse_float_value(text):
    if text is None:
        return None
    s=text.strip()
    if not s:
        return None
    lower=s.lower()
    if lower in ('na','nan'):
        return None
    if lower in ('inf','+inf'):
        return float('inf')
    if lower=='-inf':
        return float('-inf')
    try:
        return float(s)
    except ValueError:
        return None


def parse_overall_cell(cell):
    if cell is None:
        return {'actual': None, 'pct': None}
    s=cell.strip()
    if not s:
        return {'actual': None, 'pct': None}
    if '(' in s and s.endswith(')'):
        actual_part, pct_part = s.split('(', 1)
        actual_val=parse_float_value(actual_part.strip().rstrip('%'))
        pct_text=pct_part[:-1].strip()
        if pct_text.endswith('%'):
            pct_text=pct_text[:-1]
        pct_val=parse_float_value(pct_text)
        return {'actual': actual_val, 'pct': pct_val}
    if s.endswith('%'):
        actual_val=parse_float_value(s[:-1])
        return {'actual': actual_val, 'pct': None}
    actual_val=parse_float_value(s)
    return {'actual': actual_val, 'pct': None}


def value_for_excel(value):
    if value is None:
        return 0.0
    if value==float('inf'):
        return None
    return round(float(value), 3)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    ap=argparse.ArgumentParser(description='Compute performance gain percentages between base and tuned variant.')
    ap.add_argument('--sim-root',help='Path to sim_run dir (default $ACCELSIM_ROOT/../sim_run_12.1)')
    ap.add_argument('--benchmarks',nargs='*',help='Benchmarks to include (auto-discover if omitted).')
    ap.add_argument('--variants',nargs='+',required=True,help='Variants list containing base and tuned.')
    ap.add_argument('--txt-file',default='perf_gain.txt',help='Legacy TXT output file.')
    ap.add_argument('--csv-file',default='perf_gain.csv',help='CSV output file.')
    ap.add_argument('--md-file',default='perf_gain.md',help='Markdown output file.')
    ap.add_argument('--html-file',default='perf_gain.html',help='Colored HTML table output file.')
    ap.add_argument('--xlsx-file',help='Optional XLSX output file (requires openpyxl).')
    ap.add_argument('--epsilon',type=float,default=0.2,help='Percent threshold to treat as neutral (+/-). Default 0.2%%.')
    ap.add_argument('--debug-geomean',action='store_true',help='Print detailed geometric mean inputs and alternate calculations.')
    ap.add_argument('--overall-csv', default=os.path.join(SCRIPT_DIR, 'overall_perf_study.csv'), help='Aggregate CSV across studies with per-study geomean results.')
    ap.add_argument('--overall-md', default=os.path.join(SCRIPT_DIR, 'overall_perf_study.md'), help='Aggregate Markdown across studies with per-study geomean results.')
    ap.add_argument('--overall-xlsx', default=os.path.join(SCRIPT_DIR, 'overall_perf_study.xlsx'), help='Aggregate XLSX across studies (requires openpyxl).')
    ap.add_argument('--study-name', help='Override study name for overall tables (default: normalized tuned variant).')
    args=ap.parse_args()
    sim_root=os.path.expanduser(os.path.expandvars(args.sim_root)) if args.sim_root else default_sim_root()
    if not sim_root: sys.exit('[ERROR] sim-root unresolved.')
    benches=args.benchmarks if args.benchmarks else discover(sim_root)
    if not benches: sys.exit('[WARN] no benchmarks found.')
    base_variant, tuned_variant = find_base_and_tuned(args.variants)
    if not base_variant or not tuned_variant:
        sys.exit('[ERROR] unable to identify base or tuned variant (need default-config and mshr-entries-32).')
    rows=[]  # per-kernel rows raw
    avg_rows=[]  # summary rows raw
    md_rows=[]  # colored per-kernel rows
    md_avg_rows=[]  # colored avg rows
    metric_ratios={metric:[] for metric in METRIC_ORDER}
    metric_geomean_inputs={metric:{'base':[], 'tuned':[]} for metric in METRIC_ORDER}
    bench_pct_records=[]
    header_cols=['benchmark','kernel_index','ipc_base','ipc_tuned','ipc_gain_pct','read_base','read_tuned','read_change_pct','write_base','write_tuned','write_change_pct']
    csv_header_extended=header_cols + ['ipc_gain_class','read_change_class','write_change_class']
    for bench in benches:
        base_data=collect_variant(sim_root, bench, base_variant)
        tuned_data=collect_variant(sim_root, bench, tuned_variant)
        if not base_data or not tuned_data:
            continue
        kc=max(len(base_data), len(tuned_data))
        # extend shorter by repeating last
        if len(base_data)<kc and base_data:
            base_data=base_data + [base_data[-1]]*(kc-len(base_data))
        if len(tuned_data)<kc and tuned_data:
            tuned_data=tuned_data + [tuned_data[-1]]*(kc-len(tuned_data))
        ipc_gains=[]; read_changes=[]; write_changes=[]
        for i in range(kc):
            b=base_data[i]; t=tuned_data[i]
            ipc_gain=pct_change(t.get('ipc'), b.get('ipc')) if b.get('ipc') is not None and t.get('ipc') is not None else 0.0
            read_change=pct_change(t.get('r_total'), b.get('r_total'))
            write_change=pct_change(t.get('w_total'), b.get('w_total'))
            ipc_gains.append(ipc_gain); read_changes.append(read_change); write_changes.append(write_change)
            ipc_gain_str = 'inf' if ipc_gain==float('inf') else f"{ipc_gain:.3f}"
            read_change_str = 'inf' if read_change==float('inf') else f"{read_change:.3f}"
            write_change_str = 'inf' if write_change==float('inf') else f"{write_change:.3f}"
            # classification: IPC higher better (gain>0 or inf); fail counts lower better (change<0)
            ipc_good = (ipc_gain==float('inf')) or (ipc_gain is not None and ipc_gain>0)
            read_good = (read_change is not None and read_change<0)
            write_good = (write_change is not None and write_change<0)
            ipc_class = 'better' if ipc_good else ('worse' if ipc_gain<0 else 'neutral')
            read_class = 'better' if read_good else ('worse' if read_change>0 else 'neutral')
            write_class = 'better' if write_good else ('worse' if write_change>0 else 'neutral')
            rows.append([
                bench, str(i+1),
                str(b.get('ipc')), str(t.get('ipc')),
                ipc_gain_str,
                str(b.get('r_total')), str(t.get('r_total')),
                read_change_str,
                str(b.get('w_total')), str(t.get('w_total')),
                write_change_str,
                ipc_class, read_class, write_class
            ])
            # colored MD row
            def color_wrap(val, good_flag, bad_flag):
                if good_flag:
                    return f"<span style='background-color:#d4f5d4'>{val}</span>"
                if bad_flag:
                    return f"<span style='background-color:#f8d0d0'>{val}</span>"
                return val
            md_rows.append([
                bench, str(i+1),
                str(b.get('ipc')), str(t.get('ipc')),
                color_wrap(ipc_gain_str, ipc_good, (not ipc_good and ipc_gain!=0)),
                str(b.get('r_total')), str(t.get('r_total')),
                color_wrap(read_change_str, read_good, (not read_good and read_change!=0)),
                str(b.get('w_total')), str(t.get('w_total')),
                color_wrap(write_change_str, write_good, (not write_good and write_change!=0))
            ])
        bench_metric_pct={}
        for metric in METRIC_ORDER:
            key = METRIC_VALUE_KEYS[metric]
            base_geo=geometric_mean_from_records(base_data, key)
            tuned_geo=geometric_mean_from_records(tuned_data, key)
            ratio=ratio_from_geomeans(base_geo, tuned_geo)
            pct=ratio_to_pct(ratio)
            bench_metric_pct[metric]=pct
            if base_geo is not None:
                metric_geomean_inputs[metric]['base'].append(base_geo)
            if tuned_geo is not None:
                metric_geomean_inputs[metric]['tuned'].append(tuned_geo)
            if ratio is not None:
                metric_ratios[metric].append(ratio)
        avg_rows.append([
            bench,
            format_pct(bench_metric_pct.get('ipc')),
            format_pct(bench_metric_pct.get('global_acc_r')),
            format_pct(bench_metric_pct.get('global_acc_w'))
        ])
        def colorize(val, metric_type):
            display=format_pct(val)
            if val is None or display=='NA':
                return display
            if val==float('inf'):
                is_better = (metric_type=='ipc')
                is_worse = not is_better
            else:
                fv=float(val)
                if metric_type=='ipc':
                    is_better = fv>0
                    is_worse = fv<0
                else:
                    is_better = fv<0
                    is_worse = fv>0
            if is_better:
                return f"<span style='background-color:#d4f5d4'>{display}</span>"
            if is_worse:
                return f"<span style='background-color:#f8d0d0'>{display}</span>"
            return display
        ipc_val=bench_metric_pct.get('ipc')
        read_val=bench_metric_pct.get('global_acc_r')
        write_val=bench_metric_pct.get('global_acc_w')
        md_avg_rows.append([
            bench,
            colorize(ipc_val,'ipc'),
            colorize(read_val,'global_acc_r'),
            colorize(write_val,'global_acc_w')
        ])
        bench_pct_records.append((bench, bench_metric_pct))
    # Build overall summary from avg_rows
    ipc_geo_pct = rd_geo_pct = wr_geo_pct = None
    metric_geo_base={}
    metric_geo_tuned={}
    overall_lines=[]
    overall_summary_rows=[]
    overall_metric_map={}
    overall_order=[]
    if bench_pct_records:
        eps=args.epsilon
        metric_geo_pct={}
        for metric in METRIC_ORDER:
            inputs=metric_geomean_inputs[metric]
            base_geo=geometric_mean(inputs['base'])
            tuned_geo=geometric_mean(inputs['tuned'])
            ratio=ratio_from_geomeans(base_geo, tuned_geo)
            metric_geo_pct[metric]=ratio_to_pct(ratio)
            metric_geo_base[metric]=base_geo
            metric_geo_tuned[metric]=tuned_geo
        overall_lines=['GEOMETRIC MEAN SUMMARY']
        overall_lines.append(f"IPC geomean percent change: {format_pct(metric_geo_pct.get('ipc'))}%")
        overall_lines.append(f"GLOBAL_ACC_R geomean percent change: {format_pct(metric_geo_pct.get('global_acc_r'))}%")
        overall_lines.append(f"GLOBAL_ACC_W geomean percent change: {format_pct(metric_geo_pct.get('global_acc_w'))}%")

        def count_wins(metric, better_is_greater):
            wins=losses=neutrals=0
            for _, pct_map in bench_pct_records:
                val=pct_map.get(metric)
                if val is None:
                    neutrals+=1
                    continue
                if val==float('inf'):
                    if better_is_greater:
                        wins+=1
                    else:
                        losses+=1
                    continue
                if abs(val)<=eps:
                    neutrals+=1
                elif val>0:
                    if better_is_greater:
                        wins+=1
                    else:
                        losses+=1
                else:
                    if better_is_greater:
                        losses+=1
                    else:
                        wins+=1
            return wins, losses, neutrals
        ipc_w, ipc_l, ipc_n = count_wins('ipc', True)
        rd_w, rd_l, rd_n = count_wins('global_acc_r', False)
        wr_w, wr_l, wr_n = count_wins('global_acc_w', False)
        overall_lines.append(f"GLOBAL_ACC_R win/loss/neutral benchmarks: {rd_w}/{rd_l}/{rd_n}")
        overall_lines.append(f"GLOBAL_ACC_W win/loss/neutral benchmarks: {wr_w}/{wr_l}/{wr_n}")

        ipc_geo_pct = metric_geo_pct.get('ipc')
        rd_geo_pct = metric_geo_pct.get('global_acc_r')
        wr_geo_pct = metric_geo_pct.get('global_acc_w')

        if args.debug_geomean:
            print('[DEBUG] Bench-level geomean ratios:')
            for metric, ratios in metric_ratios.items():
                print(f'  {metric}:', ratios)
            print('[DEBUG] Bench-level percent changes:')
            for bench, pct_map in bench_pct_records:
                print(f"  {bench}: ipc={pct_map.get('ipc')}%, global_acc_r={pct_map.get('global_acc_r')}%, global_acc_w={pct_map.get('global_acc_w')}%")

    # TXT legacy
    txt_lines=[' '.join(csv_header_extended)]
    txt_lines.extend([' '.join(r) for r in rows])
    txt_lines.append('')
    txt_lines.append('benchmark ipc_gain_pct read_change_pct write_change_pct')
    for a in avg_rows:
        txt_lines.append(f"{a[0]} {a[1]} {a[2]} {a[3]}")
    if overall_lines:
        txt_lines.append('')
        txt_lines.extend(overall_lines)
    with open(args.txt_file,'w') as f:
        f.write('\n'.join(txt_lines))
    print(f"[INFO] wrote {args.txt_file}")
    # CSV
    import csv
    with open(args.csv_file,'w',newline='') as cf:
        w=csv.writer(cf)
        w.writerow(csv_header_extended)
        for r in rows: w.writerow(r)
        w.writerow([])
        w.writerow(['benchmark','ipc_gain_pct','read_change_pct','write_change_pct'])
        for a in avg_rows:
            w.writerow([a[0],a[1],a[2],a[3]])
        if overall_lines:
            w.writerow([])
            w.writerow(['OVERALL','ipc_geomean_pct','global_acc_r_geomean_pct','global_acc_w_geomean_pct'])
            w.writerow(['OVERALL', format_pct(ipc_geo_pct), format_pct(rd_geo_pct), format_pct(wr_geo_pct)])
    print(f"[INFO] wrote {args.csv_file}")
    # Markdown
    md_lines=[
        "# Performance Gain Report",
        "",
        "## Per-Kernel Details (colored)",
        "",
        '|'+'|'.join(header_cols)+'|',
        '|'+'|'.join(['---']*len(header_cols))+'|'
    ]
    for r in md_rows:
        md_lines.append('|'+'|'.join(r)+'|')
    md_lines.append('')
    md_lines.append('## Averages')
    md_lines.append('')
    md_lines.append('|benchmark|ipc_gain_pct|read_change_pct|write_change_pct|')
    md_lines.append('|---|---|---|---|')
    for a in md_avg_rows:
        md_lines.append(f"|{a[0]}|{a[1]}|{a[2]}|{a[3]}|")
    if overall_lines:
        md_lines.append('')
        md_lines.append('## Overall Summary')
        md_lines.append('')
        md_lines.append(f"- IPC geomean percent change: <b>{format_pct(ipc_geo_pct)}%</b>")
        md_lines.append(f"- GLOBAL_ACC_R geomean percent change: <b>{format_pct(rd_geo_pct)}%</b>")
        md_lines.append(f"- GLOBAL_ACC_W geomean percent change: <b>{format_pct(wr_geo_pct)}%</b>")
    with open(args.md_file,'w') as mf:
        mf.write('\n'.join(md_lines))
    print(f"[INFO] wrote {args.md_file}")

    # HTML colored output
    html_lines=["<html><head><meta charset='utf-8'><title>Performance Gain Report</title><style>table{border-collapse:collapse;font-family:monospace;} td,th{border:1px solid #888;padding:4px;} .better{background:#d4f5d4;} .worse{background:#f8d0d0;} .neutral{background:#f0f0f0;}</style></head><body>","<h1>Performance Gain Report</h1>"]
    html_lines.append('<h2>Per-Kernel Details</h2>')
    html_lines.append('<table>')
    html_lines.append('<tr>' + ''.join(f'<th>{c}</th>' for c in header_cols) + '</tr>')
    # map md_rows (no class info) -> need classification from rows list
    for raw, colored in zip(rows, md_rows):
        ipc_class=raw[-3]; read_class=raw[-2]; write_class=raw[-1]
        # colored list has no class columns, rebuild row with classes applied to gain/change cells
        html_lines.append('<tr>' +
            f'<td>{raw[0]}</td><td>{raw[1]}</td>' +
            f'<td>{raw[2]}</td><td>{raw[3]}</td>' +
            f'<td class="{ipc_class}">{raw[4]}</td>' +
            f'<td>{raw[5]}</td><td>{raw[6]}</td>' +
            f'<td class="{read_class}">{raw[7]}</td>' +
            f'<td>{raw[8]}</td><td>{raw[9]}</td>' +
            f'<td class="{write_class}">{raw[10]}</td>' +
            '</tr>')
    html_lines.append('</table>')
    html_lines.append('<h2>Averages</h2>')
    html_lines.append('<table>')
    html_lines.append('<tr><th>benchmark</th><th>ipc_gain_pct</th><th>read_change_pct</th><th>write_change_pct</th></tr>')
    def classify_metric(val, metric_type):
        if val is None:
            return 'neutral'
        if val==float('inf'):
            return 'better' if metric_type=='ipc' else 'worse'
        if metric_type=='ipc':
            return 'better' if val>0 else ('worse' if val<0 else 'neutral')
        return 'better' if val<0 else ('worse' if val>0 else 'neutral')

    for (bench, pct_map), a_raw, _ in zip(bench_pct_records, avg_rows, md_avg_rows):
        ipc_val_num=pct_map.get('ipc')
        read_val_num=pct_map.get('global_acc_r')
        write_val_num=pct_map.get('global_acc_w')
        ipc_val=a_raw[1]; read_val=a_raw[2]; write_val=a_raw[3]
        ipc_class = classify_metric(ipc_val_num, 'ipc')
        read_class = classify_metric(read_val_num, 'global_acc_r')
        write_class = classify_metric(write_val_num, 'global_acc_w')
        html_lines.append('<tr>' +
            f'<td>{bench}</td>' +
            f'<td class="{ipc_class}">{ipc_val}</td>' +
            f'<td class="{read_class}">{read_val}</td>' +
            f'<td class="{write_class}">{write_val}</td>' +
            '</tr>')
    if overall_lines:
        html_lines.append('</table>')
        html_lines.append('<h2>Overall Summary</h2>')
        html_lines.append('<ul>')
        html_lines.append(f"<li>IPC geomean percent change: <b>{format_pct(ipc_geo_pct)}%</b></li>")
        html_lines.append(f"<li>GLOBAL_ACC_R geomean percent change: <b>{format_pct(rd_geo_pct)}%</b></li>")
        html_lines.append(f"<li>GLOBAL_ACC_W geomean percent change: <b>{format_pct(wr_geo_pct)}%</b></li>")
        # html_lines.append(f"<li>Kernel-flatten IPC geomean (weight=1 per kernel): <b>{kernel_geo_pct:.3f}%</b></li>")
        # No calculation steps in HTML
        html_lines.append('</ul>')
    html_lines.append('</table></body></html>')
    with open(args.html_file,'w') as hf:
        hf.write('\n'.join(html_lines))
    print(f"[INFO] wrote {args.html_file}")

    # Update overall study tables aggregating multiple studies
    if overall_lines:
        tuned_name = normalize_variant_name(tuned_variant)
        study_name = args.study_name if args.study_name else tuned_name
        header_labels = ['study'] + [f"{METRIC_LABELS.get(metric, metric)} (geomean)" for metric in METRIC_ORDER]

        def ensure_metric_map(entry=None):
            entry = dict(entry) if entry else {}
            for metric in METRIC_ORDER:
                entry.setdefault(metric, {'actual': None, 'pct': None})
            return entry

        # Load existing CSV if present
        existing = {}
        if os.path.isfile(args.overall_csv):
            import csv as _csv
            with open(args.overall_csv, 'r', newline='') as f:
                rdr = _csv.reader(f)
                hdr = next(rdr, None)
                for row in rdr:
                    if not row or row[0].startswith('#'):
                        continue
                    study = row[0].strip()
                    if not study:
                        continue
                    metric_map = {}
                    for idx, metric in enumerate(METRIC_ORDER, start=1):
                        cell = row[idx] if idx < len(row) else ''
                        metric_map[metric] = parse_overall_cell(cell)
                    existing[study] = ensure_metric_map(metric_map)

        base_entry = ensure_metric_map(existing.get('base-config'))
        for metric in METRIC_ORDER:
            base_entry[metric] = {'actual': metric_geo_base.get(metric), 'pct': None}
        existing['base-config'] = base_entry

        study_entry = ensure_metric_map(existing.get(study_name))
        for metric in METRIC_ORDER:
            study_entry[metric] = {'actual': metric_geo_tuned.get(metric), 'pct': metric_geo_pct.get(metric)}
        existing[study_name] = study_entry

        # Ensure all studies have all metrics
        for study in list(existing.keys()):
            existing[study] = ensure_metric_map(existing.get(study))

        order = ['base-config'] + sorted([k for k in existing.keys() if k!='base-config'])
        overall_order = order
        overall_metric_map = {study: ensure_metric_map(existing.get(study)) for study in order}
        formatted_overall_rows=[]
        for study in order:
            metric_map = overall_metric_map[study]
            cells=[]
            for metric in METRIC_ORDER:
                entry = metric_map[metric]
                include_pct = (study!='base-config' and entry['pct'] is not None)
                cells.append(format_actual_with_pct(entry['actual'], entry['pct'], include_pct))
            formatted_overall_rows.append((study, cells))
        overall_summary_rows = [header_labels] + [[study] + cells for study, cells in formatted_overall_rows]

        # Write CSV
        import csv as _csv
        with open(args.overall_csv,'w',newline='') as f:
            w=_csv.writer(f)
            w.writerow(header_labels)
            for study, cells in formatted_overall_rows:
                w.writerow([study] + cells)
        print(f"[INFO] updated {args.overall_csv}")

        # Write Markdown
        md2 = [
            '# Overall Performance Study',
            '',
            '|study|' + '|'.join(f"{METRIC_LABELS.get(metric, metric)} (geomean)" for metric in METRIC_ORDER) + '|',
            '|---|' + '|'.join(['---:']*len(METRIC_ORDER)) + '|'
        ]
        for study, cells in formatted_overall_rows:
            md2.append(f"|{study}|{'|'.join(cells)}|")
        with open(args.overall_md,'w') as f:
            f.write('\n'.join(md2))
        print(f"[INFO] updated {args.overall_md}")

        # Write XLSX (optional)
        try:
            from openpyxl import Workbook as _WB
            from openpyxl.styles import PatternFill as _PF
            wb=_WB(); ws=wb.active; ws.title='Overall'
            ws.append(header_labels)
            for study, cells in formatted_overall_rows:
                ws.append([study] + cells)
            green='FFD4F5D4'; red='FFF8D0D0'; grey='FFF0F0F0'
            for idx, study in enumerate(order, start=2):
                metric_map = overall_metric_map[study]
                for col_offset, metric in enumerate(METRIC_ORDER, start=2):
                    entry = metric_map[metric]
                    pct_val = entry['pct']
                    if study=='base-config' or pct_val is None:
                        fill_color = grey
                    elif pct_val == float('inf'):
                        fill_color = green if metric=='ipc' else red
                    else:
                        if metric=='ipc':
                            fill_color = green if pct_val>0 else red if pct_val<0 else grey
                        else:
                            fill_color = green if pct_val<0 else red if pct_val>0 else grey
                    ws.cell(row=idx, column=col_offset).fill=_PF(fill_type='solid', fgColor=fill_color)
            wb.save(args.overall_xlsx)
            print(f"[INFO] updated {args.overall_xlsx}")
        except ImportError:
            print('[WARN] openpyxl not installed; skipping overall XLSX output.')

    # Optional XLSX output
    if args.xlsx_file:
        try:
            from openpyxl import Workbook
            from openpyxl.styles import PatternFill
            from openpyxl.formatting.rule import CellIsRule
            wb=Workbook(); ws=wb.active; ws.title='PerKernel'
            # header extended
            ws.append(csv_header_extended)
            # Use ARGB colors with full opacity for better compatibility
            color_map={'better':'FFD4F5D4','worse':'FFF8D0D0','neutral':'FFF0F0F0'}
            for r in rows:
                ws.append(r)
                # apply fill to classified cells (ipc_gain_pct at col5, read_change_pct at col8, write_change_pct at col11)
                last_row=ws.max_row
                ipc_cell=ws.cell(row=last_row,column=5); ipc_cell.fill=PatternFill(fill_type='solid', fgColor=color_map[r[-3]])
                read_cell=ws.cell(row=last_row,column=8); read_cell.fill=PatternFill(fill_type='solid', fgColor=color_map[r[-2]])
                write_cell=ws.cell(row=last_row,column=11); write_cell.fill=PatternFill(fill_type='solid', fgColor=color_map[r[-1]])
            # Add conditional formatting (works in LibreOffice/Excel)
            green_fill=PatternFill(fill_type='solid', fgColor=color_map['better'])
            red_fill=PatternFill(fill_type='solid', fgColor=color_map['worse'])
            # IPC: greaterThan 0 -> green, lessThan 0 -> red
            if ws.max_row >= 2:
                ws.conditional_formatting.add(f"E2:E{ws.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=green_fill))
                ws.conditional_formatting.add(f"E2:E{ws.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=red_fill))
                # READ fails: lessThan 0 -> green, greaterThan 0 -> red
                ws.conditional_formatting.add(f"H2:H{ws.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws.conditional_formatting.add(f"H2:H{ws.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
                # WRITE fails
                ws.conditional_formatting.add(f"K2:K{ws.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws.conditional_formatting.add(f"K2:K{ws.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
            ws2=wb.create_sheet('Averages')
            ws2.append(['benchmark','ipc_gain_pct','read_change_pct','write_change_pct'])
            for bench, pct_map in bench_pct_records:
                ipc_val_num=pct_map.get('ipc')
                read_val_num=pct_map.get('global_acc_r')
                write_val_num=pct_map.get('global_acc_w')
                ws2.append([
                    bench,
                    value_for_excel(ipc_val_num),
                    value_for_excel(read_val_num),
                    value_for_excel(write_val_num)
                ])
                lr=ws2.max_row
                def classify(val, kind):
                    if val is None:
                        return 'neutral'
                    if val==float('inf'):
                        return 'better' if kind=='ipc' else 'worse'
                    if kind=='ipc':
                        return 'better' if val>0 else ('worse' if val<0 else 'neutral')
                    return 'better' if val<0 else ('worse' if val>0 else 'neutral')
                ipc_c=classify(ipc_val_num,'ipc'); read_c=classify(read_val_num,'read'); write_c=classify(write_val_num,'write')
                ws2.cell(row=lr,column=2).fill=PatternFill(fill_type='solid', fgColor=color_map[ipc_c])
                ws2.cell(row=lr,column=3).fill=PatternFill(fill_type='solid', fgColor=color_map[read_c])
                ws2.cell(row=lr,column=4).fill=PatternFill(fill_type='solid', fgColor=color_map[write_c])
            avg_section_last_row = ws2.max_row
            if overall_summary_rows:
                ws2.append([])
                summary_header_row = ws2.max_row + 1
                if overall_summary_rows:
                    copied_styles=False
                    try:
                        from openpyxl import load_workbook as _load_wb
                        overall_wb=_load_wb(args.overall_xlsx)
                        overall_ws=overall_wb['Overall']
                        for row in overall_ws.iter_rows(values_only=False):
                            values=[cell.value for cell in row[:len(header_labels)]]
                            ws2.append(values)
                            dest_row=ws2.max_row
                            for col_idx, src_cell in enumerate(row[:len(header_labels)], start=1):
                                ws2.cell(row=dest_row, column=col_idx).fill=copy(src_cell.fill)
                        copied_styles=True
                    except Exception as exc:
                        print(f"[WARN] unable to copy overall XLSX formatting into perf_gain.xlsx: {exc}")
                    if not copied_styles:
                        for row in overall_summary_rows:
                            ws2.append(row)
                ws2.conditional_formatting.add(f"B2:B{avg_section_last_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"B2:B{avg_section_last_row}", CellIsRule(operator='lessThan', formula=['0'], fill=red_fill))
                ws2.conditional_formatting.add(f"C2:C{avg_section_last_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"C2:C{avg_section_last_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
                ws2.conditional_formatting.add(f"D2:D{avg_section_last_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"D2:D{avg_section_last_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
            wb.save(args.xlsx_file)
            print(f"[INFO] wrote {args.xlsx_file}")
        except ImportError:
            print('[WARN] openpyxl not installed; skipping XLSX output.')

if __name__=='__main__':
    main()
