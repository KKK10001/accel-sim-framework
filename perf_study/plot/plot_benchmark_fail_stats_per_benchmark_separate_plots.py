#!/usr/bin/env python3
"""
plot_benchmark_fail_stats_per_benchmark_separate_plots.py

Each benchmark -> three separate PNG files:
  <bench>_ipc.png
  <bench>_l1d_fail_global_acc_r.png
  <bench>_l1d_fail_global_acc_w.png
Variants adjacent per kernel.

example usage:
python plot_benchmark_fail_stats_per_benchmark_separate_plots.py \
    --sim-root $ACCELSIM_ROOT/../sim_run_12.1 \
    --variants regress-default-config regress-mshr-entries-32-again
"""
import argparse, os, re, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from typing import List, Dict
from matplotlib.patches import Patch

GPU_IPC_RE=re.compile(r"gpu_ipc\s*=\s*([0-9]+\.?[0-9]*)")
TOTAL_R_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\s*=\s*([0-9]+)")
TOTAL_W_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\s*=\s*([0-9]+)")
CAUSE_R_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\[(.+?)\]\s*=\s*([0-9]+)")
CAUSE_W_RE=re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\[(.+?)\]\s*=\s*([0-9]+)")

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
            for _ in range(mc-len(l)): l.append(l[-1])
    return mc

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

def plot_ipc(bench,data,variants,kc,out_root_dir):
    # ensure subfolder ipc
    out_dir=os.path.join(out_root_dir,'ipc'); os.makedirs(out_dir,exist_ok=True)
    xs=list(range(kc)); fig,ax=plt.subplots(figsize=(max(6,kc*0.9),3))
    span=0.8; vcnt=len(variants); vspan=span/vcnt; gap=vspan*0.15; width=vspan-gap
    colors={variants[0]:'#1f77b4'}; len(variants)>1 and colors.setdefault(variants[1],'#d62728')
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
    colors={variants[0]:'#1f77b4'}; len(variants)>1 and colors.setdefault(variants[1],'#d62728')
    # collect reasons
    all=set()
    for v in variants:
        for rec in data.get(v,[]): all.update(rec[f'{kind}_reasons'].keys())
    cycle=['/','\\','x','-','+','.']
    h={r:cycle[i%len(cycle)] for i,r in enumerate(sorted(all))}
    for ki in range(kc):
        for vi,v in enumerate(variants):
            recs=data.get(v,[]);
            if ki>=len(recs): continue
            rec=recs[ki]; total=rec.get(f'{kind}_total',0)
            if total<=0: continue
            x=xs[ki]-span/2+vi*vspan+gap/2+width/2
            b=0
            for rea,val in sorted(rec[f'{kind}_reasons'].items()):
                if val==0: continue
                ax.bar(x,val,width=width,bottom=b,color=colors[v],hatch=h.get(rea,'/'),edgecolor='black'); b+=val
    ax.set_xticks(xs); ax.set_xticklabels([f'k{ki+1}' for ki in xs],rotation=20)
    ax.set_ylabel('Fail counts'); title_map={'r':'GLOBAL_ACC_R','w':'GLOBAL_ACC_W'}
    ax.set_title(f'{bench} {title_map[kind]} fails')
    mq= h.get('MISS_QUEUE_FULL','/')
    handles=[Patch(facecolor=colors.get(v,'#999'),hatch=mq,edgecolor='black') for v in variants[:2]]
    labels=[f"MISS_QUEUE_FULL {norm_variant(v)}" for v in variants[:2]]
    ax.legend(handles,labels,fontsize='x-small')
    fig.tight_layout(); fname=f'{bench}_l1d_fail_global_acc_{"r" if kind=="r" else "w"}.png'
    fig.savefig(os.path.join(out_dir,fname),dpi=150); plt.close(fig)

def main():
    ap=argparse.ArgumentParser(description='Separate plots per benchmark (IPC, read fails, write fails).')
    ap.add_argument('--sim-root',help='Path to sim_run_<ver> (default $ACCELSIM_ROOT/../sim_run_12.1)')
    ap.add_argument('--benchmarks',nargs='*',help='Benchmarks (omit to auto-discover).')
    ap.add_argument('--variants',nargs='+',required=True,help='Variant tags.')
    ap.add_argument('--output-dir',help='Destination directory (default ./per-benchmark-separate-plots)')
    args=ap.parse_args()
    env=os.getenv('ACCELSIM_ROOT'); root=os.path.expanduser(os.path.expandvars(args.sim_root)) if args.sim_root else (os.path.abspath(os.path.join(env,'..','sim_run_12.1')) if env else '')
    if not root: sys.exit('[ERROR] sim-root unresolved')
    benches=args.benchmarks if args.benchmarks else [d for d in os.listdir(root) if 'rodinia-2.0-ft' in d and os.path.isdir(os.path.join(root,d))]
    if not benches: sys.exit('[WARN] no benchmarks found')
    out_dir = args.output_dir or './per-benchmark-separate-plots'
    os.makedirs(out_dir,exist_ok=True)
    # create subfolders if not exist
    for sf in ['ipc','global_acc_r','global_acc_w']:
        os.makedirs(os.path.join(out_dir,sf),exist_ok=True)
    for b in benches:
        data=collect(root,b,args.variants); kc=ensure(data)
        if kc==0: continue
        plot_ipc(b,data,args.variants,kc,out_dir)
        plot_fail(b,data,args.variants,kc,out_dir,'r')
        plot_fail(b,data,args.variants,kc,out_dir,'w')
        print(f'[INFO] wrote separate plots for {b} into {out_dir}/ipc, {out_dir}/global_acc_r, {out_dir}/global_acc_w')

if __name__=='__main__': main()
