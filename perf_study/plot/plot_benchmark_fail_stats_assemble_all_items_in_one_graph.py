#!/usr/bin/env python3
"""
plot_benchmark_fail_stats_assemble_all_items_in_one_graph.py

Original “all-in-one” plot: each benchmark → one figure; kernels on X; for each kernel
three metric groups (IPC, Read fail stack, Write fail stack) with variants adjacent.
Custom legend 3 rows x 2 columns (IPC / rd MISS_QUEUE_FULL / wr MISS_QUEUE_FULL).
"""
import argparse, os, re, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import List, Dict
from matplotlib.patches import Patch

GPU_IPC_RE = re.compile(r"gpu_ipc\s*=\s*([0-9]+\.?[0-9]*)")
TOTAL_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\s*=\s*([0-9]+)")
TOTAL_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\s*=\s*([0-9]+)")
CAUSE_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\[(.+?)\]\s*=\s*([0-9]+)")
CAUSE_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\[(.+?)\]\s*=\s*([0-9]+)")

def pick_latest_o_file(variant_dir: str) -> str:
    pat = re.compile(r".*\.o(\d+)?$")
    files = [f for f in os.listdir(variant_dir) if pat.match(f)] if os.path.isdir(variant_dir) else []
    paths = [os.path.join(variant_dir, f) for f in files]
    if not paths: return ''
    paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return paths[0]

def parse_o_file(path: str):
    try: lines = open(path).read().splitlines()
    except Exception: return []
    kernels=[]; current=None
    last_r_total=0; last_w_total=0; last_r_reasons={}; last_w_reasons={}
    def commit():
        if current is not None:
            current['r_total']=last_r_total; current['w_total']=last_w_total
            current['r_reasons']=dict(last_r_reasons); current['w_reasons']=dict(last_w_reasons)
            kernels.append(current)
    for line in lines:
        m=GPU_IPC_RE.search(line)
        if m:
            commit(); current={'ipc':float(m.group(1))}; continue
        m=TOTAL_R_RE.search(line);  m and (last_r_total:=int(m.group(1)))
        m=TOTAL_W_RE.search(line);  m and (last_w_total:=int(m.group(1)))
        m=CAUSE_R_RE.search(line); m and (last_r_reasons.__setitem__(m.group(1), int(m.group(2))))
        m=CAUSE_W_RE.search(line); m and (last_w_reasons.__setitem__(m.group(1), int(m.group(2))))
    commit()
    if not kernels and (last_r_total or last_w_total):
        kernels=[{'ipc':None,'r_total':last_r_total,'w_total':last_w_total,'r_reasons':dict(last_r_reasons),'w_reasons':dict(last_w_reasons)}]
    return kernels

def collect(sim_root:str, bench:str, variants:List[str]) -> Dict[str,List[Dict]]:
    out={}; bdir=os.path.join(sim_root, bench)
    if not os.path.isdir(bdir): return out
    for args_sub in os.listdir(bdir):
        ap=os.path.join(bdir,args_sub,'QV100-SASS')
        if not os.path.isdir(ap): continue
        for v in variants:
            vdir=os.path.join(ap,v)
            of=pick_latest_o_file(vdir)
            if not of: continue
            out[v]=parse_o_file(of)
    return out

def ensure_count(data:Dict[str,List[Dict]])->int:
    if not data: return 0
    mc=max(len(lst) for lst in data.values())
    for v,lst in data.items():
        if len(lst)<mc and lst:
            for _ in range(mc-len(lst)): lst.append(lst[-1])
    return mc

def norm_variant_name(tag:str)->str:
    name=tag
    if name.startswith('regress-'): name=name[len('regress-'):]
    if name.endswith('-again'): name=name[:-len('-again')]
    if name=='default-config': return 'base-config'
    return name

def identify_base_and_tuned(variants:List[str])->tuple:
    base=None; tuned=None
    for v in variants:
        nv=norm_variant_name(v)
        if nv=='base-config' and base is None:
            base=v
        if 'mshr-entries-32' in v or 'mshr-entries-32' in nv:
            tuned=v
    return base, tuned

def plot(bench:str, data:Dict[str,List[Dict]], variants:List[str], out_dir:str):
    if not data: return
    kc=ensure_count(data); kc or (print(f"[INFO] skip {bench}") or None)
    if kc==0: return
    fig, ax_ipc=plt.subplots(figsize=(max(6,kc*1.1),5)); ax_fail=ax_ipc.twinx()
    kernel_span=0.9; groups=3; gspan=kernel_span/groups; vcnt=len(variants)
    variant_span=gspan/max(1,vcnt); gap=variant_span*0.15; bw=variant_span-gap
    read_cycle=['/','\\','x','-','+','.']; write_cycle=['.','||','++','oo']
    all_r=set(); all_w=set()
    for v in variants:
        for rec in data.get(v,[]): all_r.update(rec['r_reasons'].keys()); all_w.update(rec['w_reasons'].keys())
    read_h={r:read_cycle[i%len(read_cycle)] for i,r in enumerate(sorted(all_r))}
    write_h={r:write_cycle[i%len(write_cycle)] for i,r in enumerate(sorted(all_w))}
    colors={variants[0]:'#1f77b4'}
    if len(variants)>1: colors[variants[1]]='#d62728'
    xs=list(range(kc))
    base_tag, tuned_tag = identify_base_and_tuned(variants)
    tuned_ipc_positions=[]; tuned_ipc_values=[]; base_ipc_values=[]
    for ki in range(kc):
        base=xs[ki]-kernel_span/2
        for gi,metric in enumerate(['ipc','r','w']):
            left=base+gi*gspan
            for vi,v in enumerate(variants):
                recs=data.get(v,[]); 
                if ki>=len(recs): continue
                rec=recs[ki]; x=left+vi*variant_span+gap/2 + bw/2
                if metric=='ipc' and rec.get('ipc') is not None:
                    ax_ipc.bar(x,rec['ipc'],width=bw,color=colors[v])
                    if v==tuned_tag:
                        tuned_ipc_positions.append(x)
                        tuned_ipc_values.append(rec['ipc'])
                        if base_tag and ki < len(data.get(base_tag,[])):
                            base_ipc=data[base_tag][ki].get('ipc')
                        else:
                            base_ipc=None
                        base_ipc_values.append(base_ipc)
                elif metric=='r' and rec.get('r_total',0)>0:
                    b=0
                    for reason,val in sorted(rec['r_reasons'].items()):
                        if val==0: continue
                        ax_fail.bar(x,val,width=bw,bottom=b,color=colors[v],hatch=read_h.get(reason,'/'),edgecolor='black'); b+=val
                elif metric=='w' and rec.get('w_total',0)>0:
                    b=0
                    for reason,val in sorted(rec['w_reasons'].items()):
                        if val==0: continue
                        ax_fail.bar(x,val,width=bw,bottom=b,color=colors[v],hatch=write_h.get(reason,'.'),edgecolor='black'); b+=val
    # annotate IPC gain for tuned variant relative to base
    if tuned_tag and base_tag and tuned_ipc_positions:
        for x,ipc_tuned,ipc_base in zip(tuned_ipc_positions,tuned_ipc_values,base_ipc_values):
            if ipc_base and ipc_base>0 and ipc_tuned is not None:
                gain=(ipc_tuned-ipc_base)/ipc_base*100.0
                ax_ipc.text(x, ipc_tuned*1.02, f"{gain:+.1f}%", ha='center', va='bottom', fontsize=7)
    ax_ipc.set_xticks(xs); ax_ipc.set_xticklabels([f'k{ki+1}' for ki in range(kc)])
    ax_ipc.set_ylabel('IPC'); ax_fail.set_ylabel('Fail counts')
    fig.suptitle(bench, y=0.96)
    rq=read_h.get('MISS_QUEUE_FULL','/'); wq=write_h.get('MISS_QUEUE_FULL','.')
    disp=variants[:2]
    handles=[]; labels=[]
    for v in disp: handles.append(Patch(facecolor=colors.get(v,'#999'))); labels.append(f"IPC: {norm_variant_name(v)}")
    for v in disp: handles.append(Patch(facecolor=colors.get(v,'#999'),hatch=rq,edgecolor='black')); labels.append(f"rd MISS_QUEUE_FULL: {norm_variant_name(v)}")
    for v in disp: handles.append(Patch(facecolor=colors.get(v,'#999'),hatch=wq,edgecolor='black')); labels.append(f"wr MISS_QUEUE_FULL: {norm_variant_name(v)}")
    if handles:
        ax_ipc.legend(handles,labels,ncol=2,fontsize='x-small',loc='upper left',bbox_to_anchor=(0,1.0,1,0.01),mode='expand',frameon=True)
    # headroom
    max_ipc=max([recs[ki]['ipc'] for v,recs in data.items() for ki in range(min(kc,len(recs))) if recs[ki].get('ipc') is not None] or [0])
    if max_ipc>0: ax_ipc.set_ylim(0,max_ipc*1.25)
    max_fail=max([max(recs[ki]['r_total'],recs[ki]['w_total']) for v,recs in data.items() for ki in range(min(kc,len(recs)))] or [0])
    if max_fail>0: ax_fail.set_ylim(0,max_fail*1.25)
    os.makedirs(out_dir,exist_ok=True)
    out_path=os.path.join(out_dir,f'{bench}.png'); fig.tight_layout(rect=[0,0,1,0.93]); fig.savefig(out_path,dpi=160); plt.close(fig); print(f'[INFO] wrote {out_path}')

def discover(sim_root:str)->List[str]:
    return sorted([d for d in os.listdir(sim_root) if 'rodinia-2.0-ft' in d and os.path.isdir(os.path.join(sim_root,d))])

def default_sim_root()->str:
    env=os.getenv('ACCELSIM_ROOT');
    if not env: return ''
    cand=os.path.abspath(os.path.join(env,'..','sim_run_12.1'))
    return cand if os.path.isdir(cand) else ''

def main():
    ap=argparse.ArgumentParser(description='All-in-one benchmark plots (IPC + Read/Write fail stacks).')
    ap.add_argument('--sim-root',help='Path to sim_run_<cuda_ver> (default $ACCELSIM_ROOT/../sim_run_12.1)')
    ap.add_argument('--benchmarks',nargs='*',help='Benchmark list (omit to auto-discover).')
    ap.add_argument('--variants',nargs='+',required=True,help='Variant tags.')
    ap.add_argument('--output-dir',required=True,help='Output directory.')
    args=ap.parse_args()
    sim_root=os.path.expanduser(os.path.expandvars(args.sim_root)) if args.sim_root else default_sim_root()
    if not sim_root:
        sys.exit('[ERROR] sim-root unresolved.')
    benches=args.benchmarks if args.benchmarks else discover(sim_root)
    if not benches: sys.exit('[WARN] no benchmarks found.')
    for b in benches:
        data=collect(sim_root,b,args.variants); plot(b,data,args.variants,args.output_dir)

if __name__=='__main__':
    main()
