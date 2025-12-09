#!/usr/bin/env python3
"""
Compare two Accel-Sim aggregate CSVs (from aggregate_ipc.py) and produce grouped-bar plots by case (x-axis):
- IPC
- L2_BW (GB/Sec)
- L2_total_cache_miss_rate

Usage:
    python3 util/job_launching/plot_compare_policies.py \
            --baseline util/job_launching/ipc_reg-baseline.csv \
            --variant util/job_launching/ipc_reg-l1d64.csv \
            --out-dir ~/dev/accel-sim/accel-sim-framework/sim_run_12.1/draws \
            [--horizontal] [--bench-only] [--max-label-len 48]

Notes:
- CSVs should include columns: bench,args,config,ipc and (for new plots) l2_bw,l2_total_cache_miss_rate.
- If l2_total_cache_miss_rate is absent, aggregate_ipc.py will fall back to l2_miss_rate.
"""
import argparse
import csv
import os
from typing import Dict, List, Tuple


def read_rows(csv_path: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    return rows


def key_for(row: Dict[str, str]) -> Tuple[str, str]:
    return (row.get("bench", ""), row.get("args", ""))


def to_float(x: str):
    try:
        return float(x)
    except Exception:
        return None


def make_labels(rows: List[Dict[str, str]], bench_only: bool, max_len: int) -> List[str]:
    labels: List[str] = []
    for r in rows:
        b = r.get("bench", "")
        a = r.get("args", "")
        label = b if bench_only else f"{b}\n{a}"
        if len(label) > max_len:
            label = label[: max_len - 1] + "…"
        labels.append(label)
    return labels


def paired_values(brows: List[Dict[str, str]], vmap: Dict[Tuple[str, str], Dict[str, str]], field: str):
    base_vals: List[float] = []
    var_vals: List[float] = []
    keep_idx: List[int] = []
    for i, br in enumerate(brows):
        k = key_for(br)
        vb = to_float(br.get(field, ""))
        vv = None
        if k in vmap:
            vv = to_float(vmap[k].get(field, ""))
        if vb is None or vv is None:
            continue
        base_vals.append(vb)
        var_vals.append(vv)
        keep_idx.append(i)
    return base_vals, var_vals, keep_idx


def plot_paired(labels: List[str], base_vals: List[float], var_vals: List[float], out_path: str, title: str, ylabel: str, horizontal: bool):
    # Headless-friendly backend, and gracefully skip if matplotlib isn't available
    try:
        import matplotlib
        if os.environ.get("MPLBACKEND", "") == "" and os.environ.get("DISPLAY", "") == "":
            matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except Exception as e:
        print(f"matplotlib not available ({e}); skipping plot {out_path}")
        return

    n = len(base_vals)
    if n == 0:
        print(f"No values for {title}; skipping {out_path}")
        return

    if horizontal:
        fig_h = max(4, n * 0.5)
        fig_w = 10
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        y = np.arange(n)
        h = 0.4
        ax.barh(y - h/2, base_vals, height=h, color="#4C78A8", label="baseline")
        ax.barh(y + h/2, var_vals, height=h, color="#F58518", label="variant")
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_xlabel(ylabel)
        ax.set_title(title)
        ax.grid(axis="x", linestyle=":", alpha=0.5)
        ax.legend()
    else:
        fig_w = max(8, n * 0.6)
        fig, ax = plt.subplots(figsize=(fig_w, 4))
        x = np.arange(n)
        w = 0.4
        ax.bar(x - w/2, base_vals, width=w, color="#4C78A8", label="baseline")
        ax.bar(x + w/2, var_vals, width=w, color="#F58518", label="variant")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(axis="y", linestyle=":", alpha=0.5)
        ax.legend()

    plt.tight_layout()
    fig.savefig(out_path, dpi=150)
    print(f"Saved {out_path}")


def write_delta_csv(out_path: str, brows, vmap, fields: List[str]):
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        import csv
        w = csv.writer(f)
        header = [
            "bench","args"
        ]
        for fld in fields:
            header += [f"{fld}_base", f"{fld}_var", f"{fld}_delta", f"{fld}_pct"]
        w.writerow(header)
        for br in brows:
            k = key_for(br)
            vr = vmap.get(k)
            if not vr:
                continue
            row = [br.get("bench",""), br.get("args","")]
            for fld in fields:
                b = to_float(br.get(fld,""))
                v = to_float(vr.get(fld,""))
                if b is None or v is None:
                    row += ["","","",""]
                else:
                    delta = v - b
                    pct = (delta / b * 100.0) if b != 0 else None
                    row += [b, v, delta, (pct if pct is not None else "")]
            w.writerow(row)


def main():
    ap = argparse.ArgumentParser(description="Compare baseline vs variant CSVs and plot paired bars")
    ap.add_argument("--baseline", required=True, help="Path to baseline CSV (from aggregate_ipc.py)")
    ap.add_argument("--variant", required=True, help="Path to variant CSV (from aggregate_ipc.py)")
    ap.add_argument("--out-prefix", default="", help="Output prefix for generated PNGs (used only if --out-dir is empty)")
    ap.add_argument(
        "--out-dir",
        default="~/dev/accel-sim/accel-sim-framework/sim_run_12.1/draws",
        help="Directory to write grouped charts (default: sim_run_12.1/draws)",
    )
    ap.add_argument("--horizontal", action="store_true", help="Use horizontal bars")
    ap.add_argument("--bench-only", action="store_true", help="Show only benchmark names in labels")
    ap.add_argument("--max-label-len", type=int, default=48, help="Maximum label length")
    args = ap.parse_args()

    b_rows = read_rows(args.baseline)
    v_rows = read_rows(args.variant)

    # Map variant rows by (bench,args)
    v_map: Dict[Tuple[str, str], Dict[str, str]] = {key_for(r): r for r in v_rows}

    # Build labels aligned to baseline order, then filter by pairs that exist in both
    labels_all = make_labels(b_rows, args.bench_only, max(8, int(args.max_label_len)))

    # Ensure output directory or prefix
    out_dir = args.out_dir.strip()
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    def out_path(name: str) -> str:
        if out_dir:
            return os.path.join(out_dir, name)
        # fallback to legacy prefix behavior
        prefix = args.out_prefix if args.out_prefix else "compare"
        return f"{prefix}_{name}"

    # IPC
    b_ipc, v_ipc, keep = paired_values(b_rows, v_map, "ipc")
    labels = [labels_all[i] for i in keep]
    plot_paired(labels, b_ipc, v_ipc, out_path("grouped_ipc.png"), "IPC (baseline vs variant)", "IPC (inst/cycle)", args.horizontal)

    # L2_BW (second figure)
    b_bw, v_bw, keep = paired_values(b_rows, v_map, "l2_bw")
    if b_bw:
        labels = [labels_all[i] for i in keep]
        plot_paired(labels, b_bw, v_bw, out_path("grouped_l2_bw.png"), "L2 Bandwidth (baseline vs variant)", "L2_BW (GB/Sec)", args.horizontal)

    # L2_total_cache_miss_rate (third figure)
    b_l2tm, v_l2tm, keep = paired_values(b_rows, v_map, "l2_total_cache_miss_rate")
    if b_l2tm:
        labels = [labels_all[i] for i in keep]
        plot_paired(labels, b_l2tm, v_l2tm, out_path("grouped_l2_total_cache_miss_rate.png"), "L2 total cache miss rate (baseline vs variant)", "Miss rate", args.horizontal)

    # Optional: legacy plots (keep for convenience)
    b_l1m, v_l1m, keep = paired_values(b_rows, v_map, "l1d_miss_rate")
    if b_l1m and not out_dir:
        labels = [labels_all[i] for i in keep]
        plot_paired(labels, b_l1m, v_l1m, out_path("l1d_miss.png"), "L1D miss rate: baseline vs variant", "Miss rate", args.horizontal)

    b_l2m, v_l2m, keep = paired_values(b_rows, v_map, "l2_miss_rate")
    if b_l2m and not out_dir:
        labels = [labels_all[i] for i in keep]
        plot_paired(labels, b_l2m, v_l2m, out_path("l2_miss.png"), "L2 miss rate: baseline vs variant", "Miss rate", args.horizontal)

    # Write a delta CSV for quick inspection
    fields = [
        "ipc",
        "l1d_hit_rate","l1d_miss_rate","l1d_total_access",
        "l2_hit_rate","l2_miss_rate","l2_total_access",
    ]
    # Delta CSV goes next to out-dir (or uses prefix)
    delta_path = os.path.join(out_dir, "grouped_delta.csv") if out_dir else (args.out_prefix + "_delta.csv")
    write_delta_csv(delta_path, b_rows, v_map, fields)


if __name__ == "__main__":
    main()
