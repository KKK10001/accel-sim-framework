#!/usr/bin/env python3
"""
Organize existing stdout/err files into a base_config subdirectory with simplified names.

What it does
- Under a sim_run root (e.g., ./sim_run_12.1), find leaf config directories
  (paths like <bench>/<args>/<config>), scan for files matching *.o<jobid> or *.e<jobid>
  at that directory level, and move them into a subdirectory 'base_config/'.
- While moving, simplify the filename by stripping the long commit/timestamp handle:
  from:  backprop-...<lots>.o91  ->  backprop-... .o91

Safety
- Only operates on files at the immediate config directory level; does not recurse
  into existing subdirectories.
- Does not modify stats.txt or other config files.

Usage
    python3 util/job_launching/organize_outputs.py \
        --run-root ./sim_run_12.1 [--config-filter QV100-SASS]
"""
import argparse
import os
import re
import shutil
from typing import Optional


def is_leaf_config_dir(path: str) -> bool:
    # Heuristic: contains gpgpusim.config or trace.config, plus stats.txt optionally
    return os.path.isfile(os.path.join(path, "gpgpusim.config")) or os.path.isfile(
        os.path.join(path, "trace.config")
    )


def simplify_name(fn: str) -> Optional[str]:
    """Simplify '<prefix>.<long-handle>.[oe]<jobid>' to '<prefix>.[oe]<jobid>'.
    We preserve the full benchmark-and-args prefix which itself may contain dots
    (e.g., 'rodinia-2.0-ft'), so we can't just split on the first dot.
    Strategy:
      1) Match final extension of the form .o<digits> or .e<digits>
      2) Remove the last dotted segment preceding that extension (the commit/time handle)
    """
    m = re.match(r"^(?P<stem>.+)\.(?P<ext>[oe]\d+)$", fn)
    if not m:
        return None
    stem = m.group("stem")
    ext = m.group("ext")
    # Remove the last dotted segment in stem
    if "." not in stem:
        # Already simplified
        return fn
    prefix = stem.rsplit(".", 1)[0]
    return f"{prefix}.{ext}"


def main():
    ap = argparse.ArgumentParser(description="Organize stdout/err into base_config with simplified names")
    ap.add_argument("--run-root", default="./sim_run_12.1")
    ap.add_argument("--config-filter", default=None, help="Only process leaf config directories whose name contains this substring")
    args = ap.parse_args()

    run_root = os.path.abspath(args.run_root)
    if not os.path.isdir(run_root):
        print(f"Run root not found: {run_root}")
        return

    moved = 0
    skipped = 0
    for root, dirs, files in os.walk(run_root):
        # Only consider leaf config directories (depth agnostic but must contain config file)
        if not is_leaf_config_dir(root):
            continue
        cfgname = os.path.basename(root)
        if args.config_filter and args.config_filter not in cfgname:
            continue
        outdir = os.path.join(root, "base_config")
        os.makedirs(outdir, exist_ok=True)
        # 1) Move legacy commit-embedded files into base_config with simplified names
        for fn in files:
            if not re.match(r"^.*\.[oe]\d+$", fn):
                continue
            # Keep only files directly under config directory
            fpath = os.path.join(root, fn)
            if not os.path.isfile(fpath):
                continue
            newname = simplify_name(fn)
            if not newname:
                skipped += 1
                continue
            dest = os.path.join(outdir, newname)
            # Disambiguate on collision
            if os.path.exists(dest):
                base, ext = os.path.splitext(newname)
                k = 1
                while os.path.exists(dest):
                    dest = os.path.join(outdir, f"{base}-dup{k}{ext}")
                    k += 1
            shutil.move(fpath, dest)
            moved += 1

        # 2) Optionally rename overly-truncated files inside base_config to the expected '<bench>-<args>.[oe]<jobid>'
        # Derive bench/args from directory tree: .../<bench>/<args>/<config>/base_config
        parts = root.split(os.sep)
        bench = parts[-3] if len(parts) >= 3 else None
        argsdir = parts[-2] if len(parts) >= 2 else None
        if bench and argsdir:
            expected_base = f"{bench}-{argsdir}"
            try:
                for fn in os.listdir(outdir):
                    m = re.match(r"^(?P<base>[^\.]+)\.(?P<ext>[oe]\d+)$", fn)
                    if not m:
                        continue
                    base = m.group("base")
                    ext = m.group("ext")
                    if base == expected_base:
                        continue
                    src = os.path.join(outdir, fn)
                    dst = os.path.join(outdir, f"{expected_base}.{ext}")
                    # Avoid clobbering existing correct-named files
                    if os.path.exists(dst):
                        # add a suffix to disambiguate
                        k = 1
                        alt = os.path.join(outdir, f"{expected_base}-dup{k}.{ext}")
                        while os.path.exists(alt):
                            k += 1
                            alt = os.path.join(outdir, f"{expected_base}-dup{k}.{ext}")
                        dst = alt
                    os.rename(src, dst)
            except Exception:
                pass
    print(f"Moved {moved} files into 'base_config' subdirectories; skipped {skipped}.")


if __name__ == "__main__":
    main()
