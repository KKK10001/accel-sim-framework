#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple


DEFAULT_ROOT = "/home/hjs/dev/accel-sim/accel-sim-framework/hw_run/device-0/12.1"
_TPC_CYCLES_ELAPSED_CANDIDATES = [
    "tpc__cycles_elapsed.sum",
    "tpc__cycles_elapsed",
]
_TPC_REG_ALLOC_STALL_CANDIDATES = [
    "tpc__warp_launch_cycles_stalled_shader_cs_reason_register_allocation.sum",
    "tpc__warp_launch_cycles_stalled_shader_cs_reason_register_allocation",
]


# User-facing alias columns (no suffix), mapped from common Nsight Compute suffixes.
ALIAS_COLS: dict[str, List[str]] = {
    "tpc__cycles_elapsed": _TPC_CYCLES_ELAPSED_CANDIDATES,
    "tpc__warp_launch_cycles_stalled_shader_cs_reason_register_allocation": _TPC_REG_ALLOC_STALL_CANDIDATES,
    "smsp__inst_issued": [
        "smsp__inst_issued.sum",
        "smsp__inst_issued",
    ],
    "smsp__cycles_elapsed": [
        "smsp__cycles_elapsed.sum",
        "smsp__cycles_elapsed",
    ],
    "smsp__inst_issued_per_issue_active": [
        "smsp__inst_issued_per_issue_active.ratio",
        "smsp__inst_issued_per_issue_active",
    ],
    "smsp__warp_issue_stalled_not_selected_per_warp_active": [
        "smsp__warp_issue_stalled_not_selected_per_warp_active.ratio",
        "smsp__warp_issue_stalled_not_selected_per_warp_active",
    ],
    "smsp__warp_issue_stalled_selected_per_warp_active": [
        "smsp__warp_issue_stalled_selected_per_warp_active.ratio",
        "smsp__warp_issue_stalled_selected_per_warp_active",
    ],
    "smsp__warp_issue_stalled_short_scoreboard_per_warp_active": [
        "smsp__warp_issue_stalled_short_scoreboard_per_warp_active.ratio",
        "smsp__warp_issue_stalled_short_scoreboard_per_warp_active",
    ],
    "smsp__warp_issue_stalled_long_scoreboard_per_warp_active": [
        "smsp__warp_issue_stalled_long_scoreboard_per_warp_active.ratio",
        "smsp__warp_issue_stalled_long_scoreboard_per_warp_active",
    ],
}

# Keep the merged CSV minimal: only these metrics (in this order).
OUTPUT_ALIAS_COLS: List[str] = [
    "tpc__cycles_elapsed",
    "tpc__warp_launch_cycles_stalled_shader_cs_reason_register_allocation",
    "smsp__inst_issued",
    "smsp__cycles_elapsed",
    "derived__smsp__inst_issued_div_smsp__cycles_elapsed",
    "smsp__inst_issued_per_issue_active",
    "smsp__warp_issue_stalled_not_selected_per_warp_active",
    "smsp__warp_issue_stalled_selected_per_warp_active",
    "smsp__warp_issue_stalled_short_scoreboard_per_warp_active",
    "smsp__warp_issue_stalled_long_scoreboard_per_warp_active",
]


@dataclass
class _SumCount:
    s: float = 0.0
    n: int = 0

    def add(self, v: Optional[float]) -> None:
        if v is None:
            return
        self.s += v
        self.n += 1

    def mean(self) -> Optional[float]:
        if self.n <= 0:
            return None
        return self.s / self.n

############################# Example usage #############################
# cd /home/hjs/dev/accel-sim/accel-sim-framework
# python3 ./util/hw_stats/collect_ncu_reports.py \
#   --root hw_run/device-0/12.1 \
#   --force \
#   --output hw_run/device-0/12.1/ncu_stats.all.csv
###########################################################################

@dataclass(frozen=True)
class ReportPaths:
    rep_file: Path
    run_dir: Path
    raw_csv_file: Path


def _eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _which(exe: str) -> Optional[str]:
    for d in os.environ.get("PATH", "").split(os.pathsep):
        if not d:
            continue
        p = Path(d) / exe
        if p.is_file() and os.access(str(p), os.X_OK):
            return str(p)
    return None


def _find_ncu(explicit: Optional[str]) -> str:
    if explicit:
        p = Path(explicit)
        if not p.is_file():
            raise FileNotFoundError(f"ncu not found: {p}")
        if not os.access(str(p), os.X_OK):
            raise PermissionError(f"ncu not executable: {p}")
        return str(p)

    env_override = os.environ.get("NCU_PATH")
    if env_override:
        return _find_ncu(env_override)

    found = _which("ncu")
    if found:
        return found

    # Common CUDA locations
    candidates: List[Path] = []
    for base in ("/usr/local/cuda", *sorted(Path("/usr/local").glob("cuda-*/"))):
        b = Path(base)
        candidates.append(b / "bin" / "ncu")
    for c in candidates:
        if c.is_file() and os.access(str(c), os.X_OK):
            return str(c)

    raise FileNotFoundError(
        "Could not find `ncu`. Put it in PATH or set NCU_PATH=/abs/path/to/ncu."
    )


def _iter_reports(root: Path) -> Iterator[ReportPaths]:
    for rep in root.rglob("ncu_stats.ncu-rep"):
        if not rep.is_file():
            continue
        run_dir = rep.parent
        raw_csv = run_dir / "ncu_stats.raw.csv"
        yield ReportPaths(rep_file=rep, run_dir=run_dir, raw_csv_file=raw_csv)


def _is_stale(raw_csv: Path, rep_file: Path) -> bool:
    """Return True if raw CSV is older than its source .ncu-rep."""

    try:
        return raw_csv.stat().st_mtime < rep_file.stat().st_mtime
    except OSError:
        return True


def _derive_metadata(root: Path, run_dir: Path) -> Tuple[str, str]:
    """Return (benchmark, args_folder).

    Expected layout under root:
      <benchmark>/<args_folder>/

    If it doesn't match, fallback to relative path pieces.
    """

    rel = run_dir.relative_to(root)
    parts = rel.parts
    benchmark = parts[0] if len(parts) >= 1 else ""
    args_folder = parts[1] if len(parts) >= 2 else ""
    return benchmark, args_folder


def _run_ncu_import(ncu: str, rep_file: Path, output_csv: Path) -> None:
    cmd = [
        ncu,
        "--import",
        str(rep_file),
        "--page",
        "raw",
        "--csv",
    ]

    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "ncu import failed for "
            f"{rep_file} (rc={proc.returncode})\n"
            f"STDERR:\n{proc.stderr.strip()}\n"
        )

    # Nsight Compute prints CSV to stdout.
    output_csv.write_text(proc.stdout, encoding="utf-8", errors="replace")


def _read_header_columns(csv_file: Path) -> List[str]:
    with csv_file.open("r", newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            # First non-empty row is the header.
            return row
    return []


def _iter_data_rows(csv_file: Path) -> Iterator[List[str]]:
    with csv_file.open("r", newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header_seen = False
        for row in reader:
            if not row:
                continue
            if not header_seen:
                header_seen = True
                continue
            yield row


def _parse_float_maybe(s: str) -> Optional[float]:
    s = (s or "").strip()
    if not s:
        return None
    # Nsight sometimes formats numbers with commas.
    s = s.replace(",", "")
    # Some metrics may include a percent sign in CSV exports.
    if s.endswith("%"):
        s = s[:-1].strip()
    try:
        return float(s)
    except ValueError:
        return None


def _first_present_value(
    idx_map: dict[str, int], row: List[str], candidates: List[str]
) -> Optional[float]:
    for name in candidates:
        i = idx_map.get(name)
        if i is None or i >= len(row):
            continue
        v = _parse_float_maybe(row[i])
        if v is not None:
            return v
    return None


def _compute_alias_value(alias: str, idx_map: dict[str, int], row: List[str]) -> str:
    candidates = ALIAS_COLS.get(alias)
    if not candidates:
        return ""
    v = _first_present_value(idx_map, row, candidates)
    return "" if v is None else f"{v:.12g}"


def _compute_alias_value_float(
    alias: str, idx_map: dict[str, int], row: List[str]
) -> Optional[float]:
    candidates = ALIAS_COLS.get(alias)
    if not candidates:
        return None
    return _first_present_value(idx_map, row, candidates)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Export Nsight Compute .ncu-rep reports to per-run CSV and merge them."
        )
    )
    parser.add_argument(
        "--root",
        default=DEFAULT_ROOT,
        help=f"Root directory to scan (default: {DEFAULT_ROOT})",
    )
    parser.add_argument(
        "--ncu",
        default=None,
        help="Path to ncu (default: resolve via NCU_PATH or PATH)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing ncu_stats.raw.csv",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=0,
        help="Process at most N reports (0 = no limit)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Merged output CSV path (default: <root>/ncu_stats.all.csv)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be done without running ncu or writing files",
    )

    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        _eprint(f"ERROR: root does not exist: {root}")
        return 2

    out_csv = (
        Path(args.output).expanduser().resolve()
        if args.output
        else (root / "ncu_stats.all.csv")
    )

    try:
        ncu = _find_ncu(args.ncu)
    except Exception as e:
        _eprint(f"ERROR: {e}")
        return 2

    reports = list(_iter_reports(root))
    reports.sort(key=lambda r: str(r.run_dir))
    if args.max_files and args.max_files > 0:
        reports = reports[: args.max_files]

    if not reports:
        _eprint(f"No ncu_stats.ncu-rep found under: {root}")
        return 1

    if args.dry_run:
        print(f"ncu: {ncu}")
        print(f"root: {root}")
        print(f"reports: {len(reports)}")
        print(f"output: {out_csv}")
        for r in reports:
            print(f"- {r.rep_file} -> {r.raw_csv_file}")
        return 0

    # Pass 1: export each rep -> raw csv (if needed).
    for idx, r in enumerate(reports, start=1):
        should_export = True
        if r.raw_csv_file.exists() and not args.force:
            if _is_stale(raw_csv=r.raw_csv_file, rep_file=r.rep_file):
                _eprint(f"[{idx}/{len(reports)}] stale -> re-export: {r.raw_csv_file}")
            else:
                _eprint(f"[{idx}/{len(reports)}] skip existing: {r.raw_csv_file}")
                should_export = False

        if should_export:
            _eprint(f"[{idx}/{len(reports)}] export: {r.rep_file}")
            try:
                _run_ncu_import(ncu=ncu, rep_file=r.rep_file, output_csv=r.raw_csv_file)
            except Exception as e:
                _eprint(f"  FAILED: {e}")
                continue

    # Pass 2: aggregate per benchmark.
    # Requirement: for each benchmark, each kernel has equal weight.
    # Implementation: group by Kernel Name -> per-kernel mean across launches,
    # then average those per-kernel means across kernels.
    per_bench_per_kernel: dict[str, dict[str, dict[str, _SumCount]]] = {}
    kernel_name_col = "Kernel Name"

    for r in reports:
        if not r.raw_csv_file.exists():
            continue

        cols = _read_header_columns(r.raw_csv_file)
        if not cols:
            continue
        idx_map = {name: i for i, name in enumerate(cols)}

        kidx = idx_map.get(kernel_name_col)
        if kidx is None:
            continue

        benchmark, _args_folder = _derive_metadata(root=root, run_dir=r.run_dir)
        if benchmark not in per_bench_per_kernel:
            per_bench_per_kernel[benchmark] = {}

        for row in _iter_data_rows(r.raw_csv_file):
            if kidx >= len(row):
                continue
            kernel_name = (row[kidx] or "").strip()
            if not kernel_name:
                continue

            per_kernel = per_bench_per_kernel[benchmark].setdefault(kernel_name, {})
            for metric in OUTPUT_ALIAS_COLS:
                sc = per_kernel.get(metric)
                if sc is None:
                    sc = _SumCount()
                    per_kernel[metric] = sc
                sc.add(_compute_alias_value_float(alias=metric, idx_map=idx_map, row=row))

    # Write aggregated CSV.
    _eprint(f"write merged CSV: {out_csv}")
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with out_csv.open("w", newline="", encoding="utf-8") as outf:
        writer = csv.writer(outf)
        writer.writerow(["benchmark", *OUTPUT_ALIAS_COLS])

        for benchmark in sorted(per_bench_per_kernel.keys()):
            kernels = per_bench_per_kernel[benchmark]
            out_row: List[str] = [benchmark]
            for metric in OUTPUT_ALIAS_COLS:
                if metric == "derived__smsp__inst_issued_div_smsp__cycles_elapsed":
                    kernel_means: List[float] = []
                    for _kname, metrics in kernels.items():
                        inst_sc = metrics.get("smsp__inst_issued")
                        cyc_sc = metrics.get("smsp__cycles_elapsed")
                        if inst_sc is None or cyc_sc is None:
                            continue
                        inst_m = inst_sc.mean()
                        cyc_m = cyc_sc.mean()
                        if inst_m is None or cyc_m is None:
                            continue
                        if cyc_m == 0:
                            continue
                        kernel_means.append(inst_m / cyc_m)
                    if not kernel_means:
                        out_row.append("")
                    else:
                        out_row.append(f"{(sum(kernel_means) / len(kernel_means)):.12g}")
                    continue
                kernel_means: List[float] = []
                for _kname, metrics in kernels.items():
                    sc = metrics.get(metric)
                    if sc is None:
                        continue
                    m = sc.mean()
                    if m is None:
                        continue
                    kernel_means.append(m)
                if not kernel_means:
                    out_row.append("")
                else:
                    out_row.append(f"{(sum(kernel_means) / len(kernel_means)):.12g}")
            writer.writerow(out_row)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
