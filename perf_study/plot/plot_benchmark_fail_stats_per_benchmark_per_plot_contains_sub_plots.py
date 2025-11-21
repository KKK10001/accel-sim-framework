#!/usr/bin/env python3
"""
plot_benchmark_fail_stats_per_benchmark_per_plot_contains_sub_plots.py

Each benchmark -> one figure with 3 horizontal subplots:
  [IPC]  [Read Fail Breakdown]  [Write Fail Breakdown]
Variants adjacent per kernel in each subplot.
"""
import argparse, os, re, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from typing import List, Dict

GPU_IPC_RE=re.compile(r"gpu_ipc\s*=\s*([0-9]+\.?[0-9]*)")
TOTAL_R_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\s*=\s*([0-9]+)")
TOTAL_W_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\s*=\s*([0-9]+)")
CAUSE_R_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\[(.+?)\]\s*=\s*([0-9]+)")
CAUSE_W_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\[(.+?)\]\s*=\s*([0-9]+)")

def pick_latest_o_file(d:str)->str:
    pat=re.compile(r".*\.o(\d+)?$");
    if not os.path.isdir(d): return ''
    c=[os.path.join(d,f) for f in os.listdir(d) if pat.match(f)]
    if not c: return ''
    c.sort(key=lambda p: os.path.getmtime(p), reverse=True); return c[0]

def parse(of:str):
    try: lines=open(of).read().splitlines()
    except: return []
    kernels=[]; cur=None; rT=0; wT=0; rR={}; wR={}
    def commit():
        if cur is not None:
            cur['r_total']=rT; cur['w_total']=wT; cur['r_reasons']=dict(rR); cur['w_reasons']=dict(wR); kernels.append(cur)
    for ln in lines:
        m=GPU_IPC_RE.search(ln)
        if m: commit(); cur={'ipc':float(m.group(1))}; continue
        m=TOTAL_R_RE.search(ln); m and (rT:=int(m.group(1)))
        m=TOTAL_W_RE.search(ln); m and (wT:=int(m.group(1)))
        m=CAUSE_R_RE.search(ln); m and (rR.__setitem__(m.group(1),int(m.group(2))))
        m=CAUSE_W_RE.search(ln); m and (wR.__setitem__(m.group(1),int(m.group(2))))
    commit()
    if not kernels and (rT or wT): kernels=[{'ipc':None,'r_total':rT,'w_total':wT,'r_reasons':dict(rR),'w_reasons':dict(wR)}]
    return kernels

def collect(root:str, bench:str, variants:List[str])->Dict[str,List[Dict]]:
    out={}; bdir=os.path.join(root,bench)
    if not os.path.isdir(bdir): return out
    for args_sub in os.listdir(bdir):
        ap=os.path.join(bdir,args_sub,'QV100-SASS')
        if not os.path.isdir(ap): continue
        for v in variants:
            vdir=os.path.join(ap,v); of=pick_latest_o_file(vdir)
            if not of: continue
            out[v]=parse(of)
    return out

def ensure(data:Dict[str,List[Dict]]):
    if not data: return 0
    m=max(len(v) for v in data.values())
    for k,l in data.items():
        if len(l)<m and l:
            for _ in range(m-len(l)): l.append(l[-1])
    return m

def norm_variant(tag:str)->str:
    if tag.startswith('regress-'): tag=tag[len('regress-'):]
    if tag.endswith('-again'): tag=tag[:-len('-again')]
    return 'base-config' if tag=='default-config' else tag

def identify_base_and_tuned(variants:List[str])->tuple:
    base=None; tuned=None
    for v in variants:
        nv=norm_variant(v)
        if nv=='base-config' and base is None:
            base=v
        if 'mshr-entries-32' in v or 'mshr-entries-32' in nv:
            tuned=v
    return base, tuned

def plot_bench(bench:str,data:Dict[str,List[Dict]],variants:List[str],out_dir:str):
    if not data: return
    kc=ensure(data); kc or (print(f'[INFO] skip {bench}') or None)
    if kc==0: return
    fig, axes=plt.subplots(1,3,figsize=(max(7,kc*1.2),4),sharex=True)
    ax_ipc, ax_r, ax_w=axes
    xs=list(range(kc))
    # variant adjacency per metric
    base_span=0.8; vcnt=len(variants); vspan=base_span/vcnt; gap=vspan*0.15; width=vspan-gap
    colors={variants[0]:'#1f77b4'};  len(variants)>1 and colors.setdefault(variants[1],'#d62728')
    # collect reasons to stack
    all_r=set(); all_w=set()
    for v in variants:
        for rec in data.get(v,[]): all_r.update(rec['r_reasons'].keys()); all_w.update(rec['w_reasons'].keys())
    r_cycle=['/','\\','x','-','+','.']; w_cycle=['.','||','++','oo']
    r_h={r:r_cycle[i%len(r_cycle)] for i,r in enumerate(sorted(all_r))}
    w_h={r:w_cycle[i%len(w_cycle)] for i,r in enumerate(sorted(all_w))}
    base_tag, tuned_tag = identify_base_and_tuned(variants)
    tuned_positions=[]; tuned_values=[]; base_values=[]
    for ki in range(kc):
        for vi,v in enumerate(variants):
            recs=data.get(v,[])
            if ki>=len(recs): continue
            rec=recs[ki]
            x_base=xs[ki]-base_span/2+vi*vspan+gap/2+width/2
            if rec.get('ipc') is not None:
                ax_ipc.bar(x_base,rec['ipc'],width=width,color=colors[v])
                if v==tuned_tag:
                    tuned_positions.append(x_base)
                    tuned_values.append(rec['ipc'])
                    if base_tag and ki < len(data.get(base_tag,[])):
                        base_values.append(data[base_tag][ki].get('ipc'))
                    else:
                        base_values.append(None)
            if rec.get('r_total',0)>0:
                b=0
                for rea,val in sorted(rec['r_reasons'].items()):
                    if val==0: continue
                    ax_r.bar(x_base,val,width=width,bottom=b,color=colors[v],hatch=r_h.get(rea,'/'),edgecolor='black'); b+=val
            if rec.get('w_total',0)>0:
                b=0
                for rea,val in sorted(rec['w_reasons'].items()):
                    if val==0: continue
                    ax_w.bar(x_base,val,width=width,bottom=b,color=colors[v],hatch=w_h.get(rea,'.'),edgecolor='black'); b+=val
    # annotate IPC gains
    if tuned_tag and base_tag and tuned_positions:
        for x,ipc_tuned,ipc_base in zip(tuned_positions,tuned_values,base_values):
            if ipc_base and ipc_base>0 and ipc_tuned is not None:
                gain=(ipc_tuned-ipc_base)/ipc_base*100.0
                ax_ipc.text(x, ipc_tuned*1.03, f"{gain:+.1f}%", ha='center', va='bottom', fontsize=7)
    ax_ipc.set_ylabel('IPC'); ax_r.set_ylabel('Read fails'); ax_w.set_ylabel('Write fails')
    for a in axes: a.set_xticks(xs); a.set_xticklabels([f'k{ki+1}' for ki in range(kc)],rotation=25)
    fig.suptitle(bench, y=0.95)
    # legend minimal (just IPC + rd/wr MISS_QUEUE_FULL) for clarity
    miss_r=r_h.get('MISS_QUEUE_FULL','/'); miss_w=w_h.get('MISS_QUEUE_FULL','.')
    from matplotlib.patches import Patch
    handles=[]; labels=[]; disp=variants[:2]
    for v in disp: handles.append(Patch(facecolor=colors.get(v,'#999'))); labels.append(f"IPC {norm_variant(v)}")
    for v in disp: handles.append(Patch(facecolor=colors.get(v,'#999'),hatch=miss_r,edgecolor='black')); labels.append(f"rd MQF {norm_variant(v)}")
    for v in disp: handles.append(Patch(facecolor=colors.get(v,'#999'),hatch=miss_w,edgecolor='black')); labels.append(f"wr MQF {norm_variant(v)}")
    ax_ipc.legend(handles,labels,ncol=2,fontsize='x-small',loc='upper left',bbox_to_anchor=(0,1.02))
    os.makedirs(out_dir,exist_ok=True)
    out=os.path.join(out_dir,f'{bench}.png'); fig.tight_layout(rect=[0,0,1,0.92]); fig.savefig(out,dpi=160); plt.close(fig); print(f'[INFO] wrote {out}')

def discover(root:str)->List[str]:
    return sorted([d for d in os.listdir(root) if 'rodinia-2.0-ft' in d and os.path.isdir(os.path.join(root,d))])

def default_root()->str:
    env=os.getenv('ACCELSIM_ROOT');
    if not env: return ''
    cand=os.path.abspath(os.path.join(env,'..','sim_run_12.1'))
    return cand if os.path.isdir(cand) else ''

def main():
    ap=argparse.ArgumentParser(description='Per benchmark figure with 3 horizontal subplots (IPC, Read, Write).')
    ap.add_argument('--sim-root',help='Path to sim_run_<ver> (default $ACCELSIM_ROOT/../sim_run_12.1)')
    ap.add_argument('--benchmarks',nargs='*',help='Benchmarks (omit to auto-discover).')
    ap.add_argument('--variants',nargs='+',required=True,help='Variant tags.')
    ap.add_argument('--output-dir',help='Destination directory (default ./per-benchmark-per-plot-contains-sub-plots)')
    args=ap.parse_args()
    root=os.path.expanduser(os.path.expandvars(args.sim_root)) if args.sim_root else default_root()
    if not root: sys.exit('[ERROR] sim-root unresolved')
    benches=args.benchmarks if args.benchmarks else discover(root)
    if not benches: sys.exit('[WARN] no benchmarks found')
    out_dir = args.output_dir or './per-benchmark-per-plot-contains-sub-plots'
    os.makedirs(out_dir,exist_ok=True)
    for b in benches:
        data=collect(root,b,args.variants); plot_bench(b,data,args.variants,out_dir)

if __name__=='__main__': main()
