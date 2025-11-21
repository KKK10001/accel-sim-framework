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
  --xlsx-file perf_gain.xlsx \
"""
import argparse, os, re, sys, math

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
    ap.add_argument('--overall-csv', default='overall_perf_study.csv', help='Aggregate CSV across studies with per-study geomean results.')
    ap.add_argument('--overall-md', default='overall_perf_study.md', help='Aggregate Markdown across studies with per-study geomean results.')
    ap.add_argument('--overall-xlsx', default='overall_perf_study.xlsx', help='Aggregate XLSX across studies (requires openpyxl).')
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
        # averages (ignore inf for averages by omitting them)
        def avg(lst):
            fl=[x for x in lst if x!=float('inf')]
            return sum(fl)/len(fl) if fl else 0.0
        avg_ipc = avg(ipc_gains); avg_read = avg(read_changes); avg_write = avg(write_changes)
        # Alternate benchmark-level IPC percent change using mean of IPCs directly rather than averaging per-kernel percent changes
        base_ipcs=[d['ipc'] for d in base_data if d.get('ipc') is not None]
        tuned_ipcs=[d['ipc'] for d in tuned_data if d.get('ipc') is not None]
        alt_ipc_pct = 0.0
        if base_ipcs and tuned_ipcs:
            base_mean=sum(base_ipcs)/len(base_ipcs)
            tuned_mean=sum(tuned_ipcs)/len(tuned_ipcs)
            if base_mean>0:
                alt_ipc_pct=(tuned_mean-base_mean)/base_mean*100.0
        avg_rows.append([
            bench,'AVG',
            f"{avg_ipc:.3f}",
            f"{avg_read:.3f}",
            f"{avg_write:.3f}"
        ])
        md_avg_rows.append([
            bench,'AVG',
            f"<span style='background-color:#d4f5d4'>{avg_ipc:.3f}</span>" if avg_ipc>0 else (f"<span style='background-color:#f8d0d0'>{avg_ipc:.3f}</span>" if avg_ipc<0 else f"{avg_ipc:.3f}"),
            f"<span style='background-color:#d4f5d4'>{avg_read:.3f}</span>" if avg_read<0 else (f"<span style='background-color:#f8d0d0'>{avg_read:.3f}</span>" if avg_read>0 else f"{avg_read:.3f}"),
            f"<span style='background-color:#d4f5d4'>{avg_write:.3f}</span>" if avg_write<0 else (f"<span style='background-color:#f8d0d0'>{avg_write:.3f}</span>" if avg_write>0 else f"{avg_write:.3f}")
        ])
        # Store alt ipc pct in parallel list for later debug
        if 'alt_ipc_list' not in globals():
            globals()['alt_ipc_list']=[]
        globals()['alt_ipc_list'].append((bench, alt_ipc_pct))
    # Build overall summary from avg_rows
    overall_lines=[]
    if avg_rows:
        eps=args.epsilon
        ipc_pcts=[float(a[2]) for a in avg_rows]
        rd_pcts=[float(a[3]) for a in avg_rows]
        wr_pcts=[float(a[4]) for a in avg_rows]
        def to_ratio_list(pcts):
            vals=[x for x in pcts if x!=float('inf') and x is not None]
            abs_vals=[abs(v) for v in vals]
            use_percent = any(v>=2.0 for v in abs_vals)
            ratios=[]
            if use_percent:
                for p in vals:
                    ratios.append(max(1.0 + p/100.0, 1e-12))
            else:
                for p in vals:
                    ratios.append(max(1.0 + p, 1e-12))
            return ratios, ('percent' if use_percent else 'fraction')
        def geomean(pcts):
            ratios,_ = to_ratio_list(pcts)
            return math.exp(sum(math.log(x) for x in ratios)/len(ratios)) if ratios else 1.0
        ipc_geo=geomean(ipc_pcts); rd_geo=geomean(rd_pcts); wr_geo=geomean(wr_pcts)
        ipc_geo_pct=(ipc_geo-1.0)*100.0
        rd_geo_pct=(rd_geo-1.0)*100.0
        wr_geo_pct=(wr_geo-1.0)*100.0
        def count_wins(pcts, better_is_greater:bool):
            wins=sum(1 for x in pcts if (x>eps if better_is_greater else x<-eps))
            losses=sum(1 for x in pcts if (x<-eps if better_is_greater else x>eps))
            neutrals=len(pcts)-wins-losses
            return wins, losses, neutrals
        ipc_w, ipc_l, ipc_n = count_wins(ipc_pcts, True)
        rd_w, rd_l, rd_n = count_wins(rd_pcts, False)
        wr_w, wr_l, wr_n = count_wins(wr_pcts, False)
        overall_lines = [
            'GEOMETRIC MEAN SUMMARY',
            f'IPC geomean percent change: {ipc_geo_pct:.3f}%',
            f'GLOBAL_ACC_R geomean percent change: {rd_geo_pct:.3f}%',
            f'GLOBAL_ACC_W geomean percent change: {wr_geo_pct:.3f}%'
        ]
        # (1) Benchmark-level geomean (each benchmark weight = 1, using ipc_pcts list)
        bench_ratios, bench_scale = to_ratio_list(ipc_pcts)
        bench_product=math.prod(bench_ratios)
        bench_root=bench_product**(1/len(bench_ratios)) if bench_ratios else 1.0
        bench_geo_pct=(bench_root-1.0)*100.0
        # (2) Kernel-flatten geomean (each kernel weight = 1). Retained for reference, not executed per request.
        # kernel_ipc_pcts=[]
        # for r in rows:
        #     val=r[4]
        #     if val=='inf':
        #         continue
        #     try:
        #         kernel_ipc_pcts.append(float(val))
        #     except ValueError:
        #         continue
        # kernel_ratios, kernel_scale = to_ratio_list(kernel_ipc_pcts)
        # kernel_product=math.prod(kernel_ratios)
        # kernel_root=kernel_product**(1/len(kernel_ratios)) if kernel_ratios else 1.0
        # kernel_geo_pct=(kernel_root-1.0)*100.0
        overall_lines.append(f'Benchmark-level IPC geomean (weights=1 per benchmark): {bench_geo_pct:.3f}%')
        # overall_lines.append(f'Kernel-flatten IPC geomean (weights=1 per kernel): {kernel_geo_pct:.3f}%')
        # Alternate geometric mean using alt benchmark ipc pct values
        alt_ipc_pcts=[v for (_,v) in globals().get('alt_ipc_list',[])]
        if alt_ipc_pcts:
            alt_geo=geomean(alt_ipc_pcts)
            alt_geo_pct=(alt_geo-1.0)*100.0
            overall_lines.append(f'IPC geomean percent change (ALT mean-of-IPC method): {alt_geo_pct:.3f}%')
        if args.debug_geomean:
            print('[DEBUG] ipc_pcts (avg of per-kernel pct changes per benchmark):', ipc_pcts)
            ratios,_dbgscale = to_ratio_list(ipc_pcts)
            print('[DEBUG] ratios from ipc_pcts:', ratios)
            print('[DEBUG] product of ratios:', math.prod(ratios))
            print(f'[DEBUG] ipc_geo ratio: {ipc_geo:.6f} -> pct {ipc_geo_pct:.6f}%')
            if alt_ipc_pcts:
                alt_ratios,_dbgscale2 = to_ratio_list(alt_ipc_pcts)
                print('[DEBUG] alt_ipc_pcts (ratio-of-means method per benchmark):', alt_ipc_pcts)
                print('[DEBUG] alt_ratios:', alt_ratios)
                print('[DEBUG] alt product of ratios:', math.prod(alt_ratios))
                print(f'[DEBUG] alt ipc_geo ratio: {alt_geo:.6f} -> pct {alt_geo_pct:.6f}%')
            print('[DEBUG] Bench-level details:')
            for (bench, altv), origv in zip(globals().get('alt_ipc_list',[]), ipc_pcts):
                print(f'  {bench}: avg_pct={origv:.6f} alt_pct={altv:.6f}')

    # TXT legacy
    txt_lines=[' '.join(csv_header_extended)]
    txt_lines.extend([' '.join(r) for r in rows])
    txt_lines.append('')
    txt_lines.append('benchmark AVG ipc_gain_pct read_change_pct write_change_pct')
    for a in avg_rows:
        txt_lines.append(f"{a[0]} {a[1]} {a[2]} {a[3]} {a[4]}")
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
        w.writerow(['benchmark','kernel_index','ipc_gain_pct','read_change_pct','write_change_pct'])
        for a in avg_rows:
            w.writerow([a[0],a[1],a[2],a[3],a[4]])
        if overall_lines:
            w.writerow([])
            w.writerow(['OVERALL','ipc_geomean_pct','global_acc_r_geomean_pct','global_acc_w_geomean_pct'])
            w.writerow(['OVERALL', f"{ipc_geo_pct:.3f}", f"{rd_geo_pct:.3f}", f"{wr_geo_pct:.3f}"])
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
    md_lines.append('|benchmark|kernel_index|ipc_gain_pct|read_change_pct|write_change_pct|')
    md_lines.append('|---|---|---|---|---|')
    for a in md_avg_rows:
        md_lines.append(f"|{a[0]}|{a[1]}|{a[2]}|{a[3]}|{a[4]}|")
    if overall_lines:
        md_lines.append('')
        md_lines.append('## Overall Summary')
        md_lines.append('')
        md_lines.append(f"- IPC geomean percent change: <b>{ipc_geo_pct:.3f}%</b>")
        md_lines.append(f"- GLOBAL_ACC_R geomean percent change: <b>{rd_geo_pct:.3f}%</b>")
        md_lines.append(f"- GLOBAL_ACC_W geomean percent change: <b>{wr_geo_pct:.3f}%</b>")
        # Add benchmark-level geomean only (kernel-flatten retained in code but not executed)
        md_lines.append(f"- Benchmark-level IPC geomean (benchmark weight=1): <b>{bench_geo_pct:.3f}%</b>")
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
    html_lines.append('<tr><th>benchmark</th><th>kernel_index</th><th>ipc_gain_pct</th><th>read_change_pct</th><th>write_change_pct</th></tr>')
    for a_raw, a_colored in zip(avg_rows, md_avg_rows):
        ipc_val=a_raw[2]; read_val=a_raw[3]; write_val=a_raw[4]
        ipc_class = 'better' if float(ipc_val)>0 else ('worse' if float(ipc_val)<0 else 'neutral')
        read_class = 'better' if float(read_val)<0 else ('worse' if float(read_val)>0 else 'neutral')
        write_class = 'better' if float(write_val)<0 else ('worse' if float(write_val)>0 else 'neutral')
        html_lines.append('<tr>' +
            f'<td>{a_raw[0]}</td><td>{a_raw[1]}</td>' +
            f'<td class="{ipc_class}">{ipc_val}</td>' +
            f'<td class="{read_class}">{read_val}</td>' +
            f'<td class="{write_class}">{write_val}</td>' +
            '</tr>')
    if overall_lines:
        html_lines.append('</table>')
        html_lines.append('<h2>Overall Summary</h2>')
        html_lines.append('<ul>')
        html_lines.append(f"<li>IPC geomean percent change: <b>{ipc_geo_pct:.3f}%</b></li>")
        html_lines.append(f"<li>GLOBAL_ACC_R geomean percent change: <b>{rd_geo_pct:.3f}%</b></li>")
        html_lines.append(f"<li>GLOBAL_ACC_W geomean percent change: <b>{wr_geo_pct:.3f}%</b></li>")
        html_lines.append(f"<li>Benchmark-level IPC geomean (weight=1 per benchmark): <b>{bench_geo_pct:.3f}%</b></li>")
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
                    if len(row) < 4:
                        continue
                    try:
                        existing[row[0]] = [float(row[1]), float(row[2]), float(row[3])]
                    except Exception:
                        continue
        # Ensure base-config row exists
        if 'base-config' not in existing:
            existing['base-config'] = [0.0, 0.0, 0.0]
        # Update current study row
        existing[study_name] = [float(f"{ipc_geo_pct:.6f}"), float(f"{rd_geo_pct:.6f}"), float(f"{wr_geo_pct:.6f}")]
        # Write CSV
        import csv as _csv
        with open(args.overall_csv,'w',newline='') as f:
            w=_csv.writer(f)
            w.writerow(['study','IPC gain (geomain)','GLOBAL_ACC_R fails (geomain)','GLOBAL_ACC_W fails (geomain)'])
            order = ['base-config'] + sorted([k for k in existing.keys() if k!='base-config'])
            for k in order:
                v=existing[k]
                w.writerow([k, f"{v[0]:.3f}", f"{v[1]:.3f}", f"{v[2]:.3f}"])
        print(f"[INFO] updated {args.overall_csv}")
        # Write Markdown
        md2 = [
            '# Overall Performance Study',
            '',
            '|study|IPC gain (geomain)|GLOBAL_ACC_R fails (geomain)|GLOBAL_ACC_W fails (geomain)|',
            '|---|---:|---:|---:|'
        ]
        for k in order:
            v=existing[k]
            md2.append(f"|{k}|{v[0]:.3f}%|{v[1]:.3f}%|{v[2]:.3f}%|")
        with open(args.overall_md,'w') as f:
            f.write('\n'.join(md2))
        print(f"[INFO] updated {args.overall_md}")
        # Write XLSX (optional)
        try:
            from openpyxl import Workbook as _WB
            from openpyxl.styles import PatternFill as _PF
            wb=_WB(); ws=wb.active; ws.title='Overall'
            ws.append(['study','IPC gain (geomain)','GLOBAL_ACC_R fails (geomain)','GLOBAL_ACC_W fails (geomain)'])
            for k in order:
                v=existing[k]
                ws.append([k, float(f"{v[0]:.3f}"), float(f"{v[1]:.3f}"), float(f"{v[2]:.3f}")])
            green='FFD4F5D4'; red='FFF8D0D0'; grey='FFF0F0F0'
            for r in range(2, ws.max_row+1):
                v=ws.cell(row=r, column=2).value
                ws.cell(row=r, column=2).fill=_PF(fill_type='solid', fgColor=(green if v>0 else (red if v<0 else grey)))
                v=ws.cell(row=r, column=3).value
                ws.cell(row=r, column=3).fill=_PF(fill_type='solid', fgColor=(green if v<0 else (red if v>0 else grey)))
                v=ws.cell(row=r, column=4).value
                ws.cell(row=r, column=4).fill=_PF(fill_type='solid', fgColor=(green if v<0 else (red if v>0 else grey)))
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
            ws2.append(['benchmark','kernel_index','ipc_gain_pct','read_change_pct','write_change_pct'])
            for a in avg_rows:
                ws2.append(a)
                lr=ws2.max_row
                def classify(val, kind):
                    v=float(val)
                    if kind=='ipc': return 'better' if v>0 else ('worse' if v<0 else 'neutral')
                    return 'better' if v<0 else ('worse' if v>0 else 'neutral')
                ipc_c=classify(a[2],'ipc'); read_c=classify(a[3],'read'); write_c=classify(a[4],'write')
                ws2.cell(row=lr,column=3).fill=PatternFill(fill_type='solid', fgColor=color_map[ipc_c])
                ws2.cell(row=lr,column=4).fill=PatternFill(fill_type='solid', fgColor=color_map[read_c])
                ws2.cell(row=lr,column=5).fill=PatternFill(fill_type='solid', fgColor=color_map[write_c])
            # Conditional formatting for averages
            if ws2.max_row >= 2:
                ws2.conditional_formatting.add(f"C2:C{ws2.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"C2:C{ws2.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=red_fill))
                ws2.conditional_formatting.add(f"D2:D{ws2.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"D2:D{ws2.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
                ws2.conditional_formatting.add(f"E2:E{ws2.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"E2:E{ws2.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
            wb.save(args.xlsx_file)
            print(f"[INFO] wrote {args.xlsx_file}")
        except ImportError:
            print('[WARN] openpyxl not installed; skipping XLSX output.')

if __name__=='__main__':
    main()
