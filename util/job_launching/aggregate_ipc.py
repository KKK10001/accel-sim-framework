#!/usr/bin/env python3
"""
Aggregate IPC across Accel-Sim/GPGPU-Sim trace-driven runs.

What it does
- Recursively scans a run root (e.g., sim_run_12.1) to find case directories
    that contain stats.txt (or stats.csv as a fallback signal), OR
- When a launch name (-N/--launch-name) is provided, it parses the corresponding
    util/job_launching/logfiles/sim_log.<launch>.*.txt to get the exact cohort of
    cases from that launch, and aggregates only those cases.
- Extracts IPC (prefer gpu_ipc/gpu_tot_ipc; else compute instr/cycle using
    common keys), plus total instructions and cycles.
- Emits a CSV summary and (optionally) a bar chart PNG if matplotlib is available.

Usage examples
    python3 util/job_launching/aggregate_ipc.py -R ./sim_run_12.1 -C QV100-SASS
    python3 util/job_launching/aggregate_ipc.py -R ./sim_run_12.1 -C QV100-SASS -o ipc_summary.csv
    python3 util/job_launching/aggregate_ipc.py -R ./sim_run_12.1 -N myTest-2025-10-30-1427 -o ipc_launch.csv -p ipc_launch.png

Notes
- Without -N, it reads the latest stats in each case directory (so if you reran a
    case later, it reflects the latest result). With -N, it aggregates the cohort
    recorded in that launch's sim_log file.
- Robust to slightly different key names across versions (gpu_ipc/gpu_tot_ipc,
    gpu_sim_insn/gpu_tot_sim_insn/TOT_INSN, gpu_sim_cycle/gpu_tot_sim_cycle/TOT_CYCLE).
"""
import argparse
import csv
import glob
import os
import re
from typing import Dict, Optional, Tuple, List, Union

# Heuristics for keys that may appear in stats.txt
IPC_KEYS = [
    # Prefer totals over instantaneous
    "gpu_tot_ipc",
    "TOT_IPC",  # sometimes only in stdout; rarely in stats.txt
    "gpu_ipc",
]
INSTR_KEYS = [
    "gpu_sim_insn",
    "gpu_tot_sim_insn",
    "gpu_total_instructions",
    "total_instructions",
    "TOT_INSN",  # sometimes only in stdout; rarely in stats.txt
]
CYCLE_KEYS = [
    "gpu_sim_cycle",
    "gpu_tot_sim_cycle",
    "total_cycles",
    "TOT_CYCLE",  # sometimes only in stdout; rarely in stats.txt
]

NAME_VALUE_RE = re.compile(r"^\s*([A-Za-z0-9_\.\-\[\]\:]+)\s*=\s*([^#\n]+)")


def parse_stats_txt(path: str) -> Dict[str, str]:
    d: Dict[str, str] = {}
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = NAME_VALUE_RE.match(line)
                if not m:
                    continue
                k = m.group(1).strip()
                v = m.group(2).strip()
                d[k] = v
    except FileNotFoundError:
        pass
    return d


def parse_gpgpu_sim_out(path: str) -> Dict[str, str]:
    """Parse stdout logs for metrics.
    Strategy:
      1) Generic name=value lines via NAME_VALUE_RE (captures gpu_ipc, gpu_tot_ipc, etc.)
      2) Fallback regex for TOT_* summary lines if present in non name=value style
    """
    d: Dict[str, str] = {}
    if not os.path.isfile(path):
        return d
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = NAME_VALUE_RE.match(line)
                if m:
                    k = m.group(1).strip()
                    v = m.group(2).strip()
                    d[k] = v
    except Exception:
        return d
    # Also try summary tokens in case they appear without key names
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        m = re.search(r"TOT_IPC\s*=\s*([0-9eE+\-\.]+)", txt)
        if m:
            d["TOT_IPC"] = m.group(1)
        m = re.search(r"TOT_INSN\s*=\s*([0-9eE+\-\.]+)", txt)
        if m:
            d["TOT_INSN"] = m.group(1)
        m = re.search(r"TOT_CYCLE\s*=\s*([0-9eE+\-\.]+)", txt)
        if m:
            d["TOT_CYCLE"] = m.group(1)
    except Exception:
        pass
    return d


def to_float(s: Optional[str]) -> Optional[float]:
    if s is None:
        return None
    try:
        # Support units like K/M/G
        ss = s.strip()
        # If the string has additional units (e.g., "GB/Sec"), extract the first float token
        m_any = re.search(r"([0-9eE+\-\.]+)", ss)
        if m_any:
            # But prefer full-match with simple suffix if possible
            m = re.match(r"^([0-9eE+\-\.]+)\s*([KMGkmg]?)$", ss)
            if m:
                val = float(m.group(1))
                suf = m.group(2).lower()
                if suf == "k":
                    val *= 1e3
                elif suf == "m":
                    val *= 1e6
                elif suf == "g":
                    val *= 1e9
                return val
            # Fall back to the first numeric token
            return float(m_any.group(1))
        return float(ss)
    except Exception:
        return None


def pick_first(d: Dict[str, str], keys: List[str]) -> Optional[str]:
    for k in keys:
        if k in d:
            return d[k]
    return None


def extract_ipc(stats: Dict[str, str]) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    # Try IPC directly
    ipc = to_float(pick_first(stats, IPC_KEYS))
    instr = to_float(pick_first(stats, INSTR_KEYS))
    cycles = to_float(pick_first(stats, CYCLE_KEYS))
    if ipc is None and instr is not None and cycles is not None and cycles > 0:
        ipc = instr / cycles
    return ipc, instr, cycles


def extract_cache_hit_rates(stats: Dict[str, str]) -> Tuple[Optional[float], Optional[float]]:
    """Compute L1D and L2 data cache hit rates from breakdown counters.
    L1D is aggregated across cores as Total_core_cache_stats_breakdown.
    L2 uses L2_cache_stats_breakdown.
    Both computed as (HIT_R + HIT_W) / (TOTAL_ACCESS_R + TOTAL_ACCESS_W).
    """
    def getf(k: str) -> Optional[float]:
        return to_float(stats.get(k))

    # L1D
    l1_r_hit = getf("Total_core_cache_stats_breakdown[GLOBAL_ACC_R][HIT]")
    l1_w_hit = getf("Total_core_cache_stats_breakdown[GLOBAL_ACC_W][HIT]")
    l1_r_tot = getf("Total_core_cache_stats_breakdown[GLOBAL_ACC_R][TOTAL_ACCESS]")
    l1_w_tot = getf("Total_core_cache_stats_breakdown[GLOBAL_ACC_W][TOTAL_ACCESS]")
    l1_rate: Optional[float] = None
    if None not in (l1_r_hit, l1_w_hit, l1_r_tot, l1_w_tot) and (l1_r_tot + l1_w_tot) > 0:
        l1_rate = (float(l1_r_hit) + float(l1_w_hit)) / (float(l1_r_tot) + float(l1_w_tot))

    # L2
    l2_r_hit = getf("L2_cache_stats_breakdown[GLOBAL_ACC_R][HIT]")
    l2_w_hit = getf("L2_cache_stats_breakdown[GLOBAL_ACC_W][HIT]")
    l2_r_tot = getf("L2_cache_stats_breakdown[GLOBAL_ACC_R][TOTAL_ACCESS]")
    l2_w_tot = getf("L2_cache_stats_breakdown[GLOBAL_ACC_W][TOTAL_ACCESS]")
    l2_rate: Optional[float] = None
    if None not in (l2_r_hit, l2_w_hit, l2_r_tot, l2_w_tot) and (l2_r_tot + l2_w_tot) > 0:
        l2_rate = (float(l2_r_hit) + float(l2_w_hit)) / (float(l2_r_tot) + float(l2_w_tot))

    return l1_rate, l2_rate


def extract_cache_totals_and_miss(stats: Dict[str, str]) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """Return (l1_total_access, l2_total_access, l1_miss_rate, l2_miss_rate).
    Miss rate is computed as 1 - hit_rate for robustness (MISS counters may be absent).
    Totals are R_TOTAL_ACCESS + W_TOTAL_ACCESS for each level.
    """
    def getf(k: str) -> Optional[float]:
        return to_float(stats.get(k))

    # L1 totals
    l1_r_tot = getf("Total_core_cache_stats_breakdown[GLOBAL_ACC_R][TOTAL_ACCESS]")
    l1_w_tot = getf("Total_core_cache_stats_breakdown[GLOBAL_ACC_W][TOTAL_ACCESS]")
    l1_total = None
    if l1_r_tot is not None or l1_w_tot is not None:
        l1_total = (l1_r_tot or 0.0) + (l1_w_tot or 0.0)

    # L2 totals
    l2_r_tot = getf("L2_cache_stats_breakdown[GLOBAL_ACC_R][TOTAL_ACCESS]")
    l2_w_tot = getf("L2_cache_stats_breakdown[GLOBAL_ACC_W][TOTAL_ACCESS]")
    l2_total = None
    if l2_r_tot is not None or l2_w_tot is not None:
        l2_total = (l2_r_tot or 0.0) + (l2_w_tot or 0.0)

    # Miss rates as 1 - hit_rate (only if hit_rate exists and totals > 0)
    l1_hit, l2_hit = extract_cache_hit_rates(stats)
    l1_miss = None if l1_hit is None else max(0.0, 1.0 - l1_hit)
    l2_miss = None if l2_hit is None else max(0.0, 1.0 - l2_hit)
    return l1_total, l2_total, l1_miss, l2_miss


def extract_l2_bw(stats: Dict[str, str]) -> Optional[float]:
    """Parse L2_BW value (typically formatted like '102.12 GB/Sec')."""
    raw = stats.get("L2_BW") or stats.get("L2_BW_total")
    return to_float(raw) if raw is not None else None


def extract_l2_total_cache_miss_rate(stats: Dict[str, str]) -> Optional[float]:
    """Prefer explicit L2_total_cache_miss_rate when available; otherwise None (caller can fallback)."""
    return to_float(stats.get("L2_total_cache_miss_rate"))


def _collect_stdout_candidates(case_dir: str) -> List[str]:
    """Collect stdout-like files from case_dir and one level of subdirectories.
    This supports layouts where *.o<jobid> files are stored under a variant subdir
    (e.g., base_config, gpgpu_unified_l1d_size_64)."""
    cand: List[str] = []
    try:
        entries = os.listdir(case_dir)
    except Exception:
        entries = []
    # Direct files in case_dir
    for p in entries:
        fp = os.path.join(case_dir, p)
        if os.path.isfile(fp):
            if p.startswith("gpgpu-sim-out_") and p.endswith(".txt"):
                cand.append(fp)
            elif re.match(r"^.*\.o\d+$", p):
                cand.append(fp)
            elif p.endswith(".out"):
                cand.append(fp)
    # One-level subdirs (variant_tag layout)
    for p in entries:
        sub = os.path.join(case_dir, p)
        if os.path.isdir(sub):
            try:
                for q in os.listdir(sub):
                    fq = os.path.join(sub, q)
                    if not os.path.isfile(fq):
                        continue
                    if q.startswith("gpgpu-sim-out_") and q.endswith(".txt"):
                        cand.append(fq)
                    elif re.match(r"^.*\.o\d+$", q):
                        cand.append(fq)
                    elif q.endswith(".out"):
                        cand.append(fq)
            except Exception:
                pass
    return cand


def find_stdout_log(case_dir: str) -> Optional[str]:
    """Return the most recent stdout-like file in a case dir (or its variant subdirs)."""
    files = _collect_stdout_candidates(case_dir)
    if not files:
        return None
    files.sort(key=lambda p: os.path.getmtime(p))
    return files[-1]


def find_stdout_log_with_handle(case_dir: str, build_handle: Optional[str]) -> Optional[str]:
    """Prefer a stdout file whose name contains the build handle for this launch.
    Fallback to the generic finder if none match.
    """
    if not build_handle:
        return find_stdout_log(case_dir)
    try:
        entries = _collect_stdout_candidates(case_dir)
    except Exception:
        entries = []
    candidates = []
    for fp in entries:
        p = os.path.basename(fp)
        if (p.startswith("gpgpu-sim-out_") and p.endswith(".txt")) or re.match(r"^.*\.o\d+$", p) or p.endswith(".out"):
            if build_handle in p:
                candidates.append(fp)
    if candidates:
        candidates.sort(key=lambda p: os.path.getmtime(p))
        return candidates[-1]
    return find_stdout_log(case_dir)


def find_stdout_log_with_job(case_dir: str, job_id: Optional[int], build_handle: Optional[str]) -> Optional[str]:
    """Prefer a stdout file that matches the specific job id (e.g., *.o<jobid>).
    Fall back to build handle matching, then to generic newest stdout.
    """
    if job_id is not None:
        try:
            entries = _collect_stdout_candidates(case_dir)
        except Exception:
            entries = []
        numeric = str(job_id)
        # Typical job stdout files are like <name>.o<jobid>
        matches = [fp for fp in entries if re.match(rf"^.*\.o{re.escape(numeric)}$", os.path.basename(fp))]
        if matches:
            matches.sort(key=lambda p: os.path.getmtime(p))
            return matches[-1]
    # fallback to handle, then generic
    return find_stdout_log_with_handle(case_dir, build_handle)


def scan_cases(run_root: str, config_filter: Optional[str]) -> List[str]:
    case_dirs: List[str] = []
    for root, dirs, files in os.walk(run_root):
        if "stats.txt" in files or "stats.csv" in files:
            if config_filter and config_filter not in root:
                continue
            case_dirs.append(root)
    return sorted(case_dirs)


SIMLOG_DIR = os.path.join(os.path.dirname(__file__), "logfiles")


def find_simlog(launch_name: str) -> Optional[str]:
    pattern = os.path.join(SIMLOG_DIR, f"sim_log.{launch_name}.*.txt")
    candidates = glob.glob(pattern)
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p))
    return candidates[-1]


def find_case_dir_by_jobid(run_root: str, job_id: int, config_filter: Optional[str]) -> Optional[str]:
    """Search run_root recursively for a stdout file *.o<jobid>.
    If config_filter is provided, restrict search to paths containing the filter.
    Return the case directory at the config level (e.g., .../<bench>/<args>/<config>),
    even if the stdout is stored under a variant subdirectory (e.g., .../<config>/baseline).
    """
    try:
        for root, dirs, files in os.walk(run_root):
            if config_filter and (config_filter not in root):
                continue
            for fn in files:
                if re.match(rf"^.*\.o{job_id}$", fn):
                    # If the match is under a variant subdir (e.g., .../<config>/<variant>),
                    # return the parent config directory for consistent labeling.
                    if config_filter:
                        base = os.path.basename(root)
                        if base == config_filter:
                            return root
                        parent = os.path.dirname(root)
                        if os.path.basename(parent) == config_filter:
                            return parent
                    # Fallback: return the directory containing the match
                    return root
    except Exception:
        pass
    return None


def parse_simlog_cases(simlog_path: str) -> List[Tuple[str, str, str, str, Optional[int]]]:
    """
    Parse lines of the form emitted by run_simulations.py logging:
      time  jobid  benchmark  args_subdir  run_subdir  build_handle
    The fields benchmark/args_subdir/run_subdir are printed as fixed-width
    columns (22/100/25). We slice using those widths after skipping time/jobid.
    Returns a list of (benchmark, args_subdir, run_subdir, build_handle).
    """
    cases: List[Tuple[str, str, str, str, Optional[int]]] = []
    try:
        with open(simlog_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            i += 1
            # Expect lines that start with time like HH:MM:SS
            if not re.match(r"^\d{2}:\d{2}:\d{2}\s+", line):
                continue
            # time (8) + spaces + jobid (<=6) + spaces
            m = re.match(r"^(\d{2}:\d{2}:\d{2})\s+(\d+)\s+(.*)$", line)
            if not m:
                continue
            job_id = None
            try:
                job_id = int(m.group(2))
            except Exception:
                job_id = None
            rest = m.group(3)
            # Some logs wrap the build handle (and sometimes the tail of runsub) onto the next line(s).
            # If the following line doesn't start with a time and contains commit tokens, append it.
            if i < len(lines) and not re.match(r"^\d{2}:\d{2}:\d{2}\s+", lines[i]):
                cont = lines[i].strip()
                if "accelsim-commit" in cont or "gpgpu-sim_git-commit" in cont:
                    rest = rest.rstrip() + " " + cont
                    i += 1
            # Pad to required width so slicing doesn't drop entries when lines are shorter due to wrapping
            need = 22 + 100 + 25
            if len(rest) < need:
                rest = rest.ljust(need)
            bench = rest[0:22].strip()
            argsdir = rest[22:122].strip()
            runsub = rest[122:147].strip()
            build_handle = rest[147:].strip()
            if bench and argsdir and runsub:
                if os.environ.get("AGG_DEBUG", ""):
                    print(f"[simlog] job={job_id} bench='{bench}' args='{argsdir}' run='{runsub}' handle='{build_handle[:32]}...'")
                cases.append((bench, argsdir, runsub, build_handle, job_id))
    except FileNotFoundError:
        pass
    return cases


def main():
    ap = argparse.ArgumentParser(description="Aggregate IPC from Accel-Sim runs")
    ap.add_argument("-R", "--run-root", default="./sim_run_12.1", help="Run root directory (default: ./sim_run_12.1)")
    ap.add_argument("-C", "--config", default=None, help="Substring filter for config dir name, e.g., QV100-SASS")
    ap.add_argument("-o", "--output-csv", default="ipc_summary.csv", help="Output CSV path")
    ap.add_argument("-N", "--launch-name", default=None, help="Restrict aggregation to cases from this launch (parse sim_log.<launch>.*.txt)")
    ap.add_argument("-p", "--plot", default="ipc_summary.png", help="Output plot PNG (set to empty to skip)")
    # Plot formatting controls
    ap.add_argument("--horizontal", action="store_true", help="Plot bars horizontally to avoid crowded x-axis")
    ap.add_argument("--bench-only", action="store_true", help="Use only the benchmark name in labels (omit args)")
    ap.add_argument("--max-label-len", type=int, default=48, help="Maximum label length; longer labels are truncated with ellipsis")
    args = ap.parse_args()

    run_root = os.path.abspath(args.run_root)
    # cases can be either list of paths or list of (path, build_handle, job_id)
    cases: List[Union[str, Tuple[str, Optional[str], Optional[int]]]] = []
    if args.launch_name:
        simlog = find_simlog(args.launch_name)
        if not simlog:
            print(f"No sim_log found for launch '{args.launch_name}' in {SIMLOG_DIR}. Falling back to directory scan.")
            cases = scan_cases(run_root, args.config)
        else:
            triplets = parse_simlog_cases(simlog)
            if not triplets:
                print(f"No cases parsed from {simlog}. Falling back to directory scan.")
                cases = scan_cases(run_root, args.config)
            else:
                # Prefer robust selection by scanning case dirs for .o* files that contain the build handle
                # seen in this launch, then filter by bench token prefixes from the sim_log to restrict cohort.
                # Resolve each case directory directly from the triplets, preserving job IDs
                tmp_cases: List[Tuple[str, Optional[str], Optional[int]]] = []
                for bench, argsdir, runsub, build_handle, job_id in triplets:
                    chosen: Optional[str] = None
                    if job_id is not None:
                        chosen = find_case_dir_by_jobid(run_root, job_id, args.config)
                    # Fallback if job-id scan failed (older logs or missing files)
                    if not chosen:
                        pattern = os.path.join(run_root, "*", argsdir.strip(), runsub.strip())
                        cand = glob.glob(pattern)
                        if cand:
                            if len(cand) == 1:
                                chosen = cand[0]
                            else:
                                bench_token = bench.replace("/", "_")
                                filtered = []
                                for pth in cand:
                                    parts = pth.split(os.sep)
                                    if len(parts) >= 3 and parts[-3].startswith(bench_token):
                                        filtered.append(pth)
                                if len(filtered) == 1:
                                    chosen = filtered[0]
                                elif filtered:
                                    filtered.sort(key=lambda p: os.path.getmtime(p))
                                    chosen = filtered[-1]
                                else:
                                    cand.sort(key=lambda p: os.path.getmtime(p))
                                    chosen = cand[-1]
                        else:
                            chosen = os.path.join(run_root, bench.replace("/", "_"), argsdir.strip(), runsub.strip())
                    if chosen and os.path.isdir(chosen) and ((not args.config) or (args.config in chosen)):
                        tmp_cases.append((chosen, build_handle, job_id))
                # Deduplicate case dirs, but keep the last seen (likely latest launch) job_id/build_handle
                uniq: Dict[str, Tuple[Optional[str], Optional[int]]] = {}
                for p, h, j in tmp_cases:
                    if os.path.isdir(p):
                        uniq[p] = (h, j)
                cases = sorted([(p, h, j) for p, (h, j) in uniq.items()])
    else:
        cases = scan_cases(run_root, args.config)
    if not cases:
        print(f"No cases found under {run_root} (config filter: {args.config})")
        return

    rows = []
    for case in cases:
        if isinstance(case, tuple):
            # Accept both (path, handle) and (path, handle, job_id)
            if len(case) == 3:
                case_dir, build_handle, job_id = case
            else:
                case_dir, build_handle = case  # type: ignore
                job_id = None
        else:
            case_dir, build_handle, job_id = case, None, None
        stats_txt = os.path.join(case_dir, "stats.txt")
        stats = parse_stats_txt(stats_txt)
        # Always merge any stdout-derived stats on top to avoid stale stats.txt from previous runs
        outlog = find_stdout_log_with_job(case_dir, job_id, build_handle)
        if outlog:
            if os.environ.get("AGG_DEBUG", ""):
                print(f"[outlog] case='{case_dir}' job_id={job_id} handle='{(build_handle or '')[:16]}...' file='{os.path.basename(outlog)}'")
            stats.update(parse_gpgpu_sim_out(outlog))
        ipc, instr, cycles = extract_ipc(stats)
        l1d_rate, l2_rate = extract_cache_hit_rates(stats)
        l1d_total, l2_total, l1d_miss, l2_miss = extract_cache_totals_and_miss(stats)
        l2_bw = extract_l2_bw(stats)
        l2_total_miss_rate = extract_l2_total_cache_miss_rate(stats)
        # If explicit total miss rate absent, fall back to computed miss rate
        if l2_total_miss_rate is None:
            l2_total_miss_rate = l2_miss

        # Derive simple labels from path
        # path .../sim_run_X/<bench>/<args>/<config>
        parts = case_dir.split(os.sep)
        bench = parts[-3] if len(parts) >= 3 else "?"
        argsdir = parts[-2] if len(parts) >= 2 else "?"
        cfg = parts[-1]
        rows.append({
            "bench": bench,
            "args": argsdir,
            "config": cfg,
            "ipc": ipc if ipc is not None else "",
            "instr": instr if instr is not None else "",
            "cycles": cycles if cycles is not None else "",
            "l1d_hit_rate": l1d_rate if l1d_rate is not None else "",
            "l2_hit_rate": l2_rate if l2_rate is not None else "",
            "l1d_miss_rate": l1d_miss if l1d_miss is not None else "",
            "l2_miss_rate": l2_miss if l2_miss is not None else "",
            "l1d_total_access": l1d_total if l1d_total is not None else "",
            "l2_total_access": l2_total if l2_total is not None else "",
            "l2_bw": l2_bw if l2_bw is not None else "",
            "l2_total_cache_miss_rate": l2_total_miss_rate if l2_total_miss_rate is not None else "",
            "case_dir": case_dir,
        })

    # Write CSV
    with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "bench",
                "args",
                "config",
                "ipc",
                "instr",
                "cycles",
                "l1d_hit_rate",
                "l2_hit_rate",
                "l1d_miss_rate",
                "l2_miss_rate",
                "l1d_total_access",
                "l2_total_access",
                "l2_bw",
                "l2_total_cache_miss_rate",
                "case_dir",
            ],
        )
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {len(rows)} rows to {args.output_csv}")

    # Optional plot
    if args.plot:
        try:
            # Use a headless backend when no DISPLAY is available to avoid GTK errors
            import matplotlib
            if os.environ.get("MPLBACKEND", "") == "" and os.environ.get("DISPLAY", "") == "":
                matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import numpy as np
            def make_label(bench: str, args_s: str) -> str:
                label = bench if args.bench_only else f"{bench}\n{args_s}"
                maxlen = max(8, int(args.max_label_len))
                if len(label) > maxlen:
                    # Keep start and end segments around the middle for readability
                    head = maxlen - 1
                    label = label[:head] + "\u2026"  # ellipsis
                return label

            labels = [make_label(r['bench'], r['args']) for r in rows]
            ipcs = []
            keep_idx = []
            for i, r in enumerate(rows):
                if r["ipc"] in ("", None):
                    continue
                try:
                    ipcs.append(float(r["ipc"]))
                    keep_idx.append(i)
                except Exception:
                    continue
            if not ipcs:
                print("No IPC values found. Skipping plot generation.")
                return
            labels = [labels[i] for i in keep_idx]
            n = len(ipcs)
            # Choose orientation
            if args.horizontal:
                fig_h = max(4, n * 0.45)
                fig_w = 8
                fig, ax = plt.subplots(figsize=(fig_w, fig_h))
                y = np.arange(n)
                ax.barh(y, ipcs, color="#4C78A8")
                ax.set_xlabel("IPC (inst/cycle)")
                ax.set_title("Accel-Sim IPC summary")
                ax.set_yticks(y)
                ax.set_yticklabels(labels, fontsize=8)
                ax.grid(axis="x", linestyle=":", alpha=0.5)
            else:
                fig_w = max(8, n * 0.6)
                fig, ax = plt.subplots(figsize=(fig_w, 4))
                x = np.arange(n)
                ax.bar(x, ipcs, color="#4C78A8")
                ax.set_ylabel("IPC (inst/cycle)")
                ax.set_title("Accel-Sim IPC summary")
                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
                ax.grid(axis="y", linestyle=":", alpha=0.5)
            plt.tight_layout()
            fig.savefig(args.plot, dpi=150)
            print(f"Saved plot to {args.plot}")
        except Exception as e:
            print(f"Skipping plot (matplotlib not available or error: {e})")


if __name__ == "__main__":
    main()
