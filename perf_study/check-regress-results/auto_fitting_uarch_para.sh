#!/usr/bin/env bash

sim_root=/home/kuanbba/dev/accel-sim/accel-sim-framework/sim_run_12.1
echo "sim_root = $sim_root"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
paths=()
paths+=( "$sim_root/backprop-rodinia-2.0-ft/4096___data_result_4096_txt/QV100-SASS" )
paths+=( "$sim_root/bfs-rodinia-2.0-ft/__data_graph4096_txt___data_graph4096_result_txt/QV100-SASS" )
paths+=( "$sim_root/heartwall-rodinia-2.0-ft/__data_test_avi_1___data_result_1_txt/QV100-SASS" )
paths+=( "$sim_root/hotspot-rodinia-2.0-ft/30_6_40___data_result_30_6_40_txt/QV100-SASS" )
paths+=( "$sim_root/lud-rodinia-2.0-ft/_v__b__i___data_64_dat/QV100-SASS" )
paths+=( "$sim_root/nw-rodinia-2.0-ft/128_10___data_result_128_10_txt/QV100-SASS" )
paths+=( "$sim_root/nn-rodinia-2.0-ft/__data_filelist_4_3_30_90___data_filelist_4_3_30_90_result_txt/QV100-SASS" )
paths+=( "$sim_root/pathfinder-rodinia-2.0-ft/1000_20_5___data_result_1000_20_5_txt/QV100-SASS" )
paths+=( "$sim_root/srad_v2-rodinia-2.0-ft/__data_matrix128x128_txt_0_127_0_127__5_2___data_result_matrix128x128_1_150_1_100__5_2_txt/QV100-SASS" )
paths+=( "$sim_root/streamcluster-rodinia-2.0-ft/3_6_16_1024_1024_100_none_output_txt_1___data_result_3_6_16_1024_1024_100_none_1_txt/QV100-SASS" )

shopt -s nullglob

regress_tags=(
    regress-default-cfg-11-25-eve
    perf-study-miss-q-ent-32-and-mshr-max-merge-32
    perf-study-miss-q-ent-64-and-mshr-max-merge-32
    perf-study-miss-q-ent-128-and-mshr-max-merge-32
    perf-study-miss-q-ent-256-and-mshr-max-merge-32
    perf-study-miss-q-ent-288-and-mshr-max-merge-32
    perf-study-miss-q-ent-320-and-mshr-max-merge-32
    perf-study-miss-q-ent-352-and-mshr-max-merge-32
    perf-study-miss-q-ent-384-and-mshr-max-merge-32
    perf-study-miss-q-ent-512-and-mshr-max-merge-32
)

fine_grained_tags=(
    # perf-study-miss-q-ent-32-and-mshr-max-merge-32
    # perf-study-miss-q-ent-64-and-mshr-max-merge-32
    # perf-study-miss-q-ent-128-and-mshr-max-merge-32 # 实际上不应该放在这里，只是为了与<mq>=256 ror对比
    perf-study-miss-q-ent-288-and-mshr-max-merge-32
    perf-study-miss-q-ent-320-and-mshr-max-merge-32
    perf-study-miss-q-ent-352-and-mshr-max-merge-32
    perf-study-miss-q-ent-384-and-mshr-max-merge-32
)

fine_grained_display_tags=()
for tag in "${fine_grained_tags[@]}"; do
    fine_grained_display_tags+=( "${tag#perf-study-}" )
done
fine_grained_variants_csv=$(IFS=','; echo "${fine_grained_display_tags[*]}")

decision_file="$script_dir/auto_fitting_decision.txt"
: > "$decision_file"

history_dir="$script_dir/history"
mkdir -p "$history_dir"
history_file="$history_dir/miss_queue_history.csv"
plot_file="$history_dir/miss_queue_full_vs_mq.png"
ror_log_file="$history_dir/ror_debug.txt"

for regress_tag in "${regress_tags[@]}"; do
    display_tag="${regress_tag#perf-study-}"
    summary_file="$script_dir/${display_tag}_fail_cause_summary.txt"
    counter=0
    zero_count=0
    missing_dirs=0
    existing_case_dirs=()

    echo "==== Processing $regress_tag ===="
    for path in "${paths[@]}"; do
        counter=$((counter + 1))
        case_dir="$path/$regress_tag"
        if [[ ! -d "$case_dir" ]]; then
            echo "[$counter] missing directory: $case_dir"
            missing_dirs=$((missing_dirs + 1))
            continue
        fi

        echo "[$counter] scanning: $case_dir"
        existing_case_dirs+=("$case_dir")
        err_files=("$case_dir"/*.e*)
        if (( ${#err_files[@]} == 0 )); then
            echo "    no *.e* files found"
            continue
        fi

        for err_file in "${err_files[@]}"; do
            size_bytes=$(stat -c%s "$err_file")
            if [[ $size_bytes -eq 0 ]]; then
                zero_count=$((zero_count + 1))
            else
                echo "    [Err!!!!!!] (${size_bytes} bytes) $err_file"
            fi
        done
    done

    echo "--- tag: $regress_tag ---"
    echo "directories scanned: $counter"
    echo "missing directories: $missing_dirs"
    echo "zero-length *.e* files: $zero_count"

    if (( ${#existing_case_dirs[@]} == 0 )); then
        echo "[WARN] no valid case directories found for variant $regress_tag; skip fail cause summary"
        {
            echo "Variant: $regress_tag"
            echo "Simulation root: $sim_root"
            echo ""
            echo "[WARN] No case directories supplied. Nothing to report."
        } > "$summary_file"
        printf 'regress_tag:%s config: {<mq>: %s, <mshr_max_merge>: %s} result: "%s" decision: "%s"\n' \
            "$display_tag" "unknown" "unknown" "No fails recorded" "stop regress" >> "$decision_file"
        continue
    fi

    python3 - "$sim_root" "$display_tag" "$summary_file" "$decision_file" "$history_file" "$plot_file" "$ror_log_file" "$fine_grained_variants_csv" "${existing_case_dirs[@]}" <<'PY'
import csv
import math
import os
import re
import sys
from collections import defaultdict, OrderedDict

TARGET_FAIL_CAUSE = 'MISS_QUEUE_FULL'

CACHE_LINE_RE = re.compile(r"-gpgpu_cache:dl1\s+(\S+)")
GPU_IPC_RE = re.compile(r"gpu_ipc\s*=\s*([0-9]+\.?[0-9]*)")
TOTAL_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\s*=\s*([0-9]+)")
TOTAL_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\s*=\s*([0-9]+)")
CAUSE_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\[(.+?)\]\s*=\s*([0-9]+)")
CAUSE_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\[(.+?)\]\s*=\s*([0-9]+)")


def pick_latest(directory: str) -> str:
    pattern = re.compile(r".*\\.o(\d+)?$")
    if not os.path.isdir(directory):
        return ''
    candidates = [os.path.join(directory, fname) for fname in os.listdir(directory) if pattern.match(fname)]
    if not candidates:
        return ''
    candidates.sort(key=lambda path: os.path.getmtime(path), reverse=True)
    return candidates[0]


def parse_log(output_file: str):
    try:
        lines = open(output_file, 'r', encoding='utf-8').read().splitlines()
    except OSError:
        return []
    records = []
    current = None
    r_total = 0
    w_total = 0
    r_reasons = {}
    w_reasons = {}
    mq_size = None
    mshr_max_merge = None

    def commit():
        if current is not None:
            current['r_total'] = r_total
            current['w_total'] = w_total
            current['r_reasons'] = dict(r_reasons)
            current['w_reasons'] = dict(w_reasons)
            current['mq_size'] = mq_size
            current['mshr_max_merge'] = mshr_max_merge
            records.append(current)

    for line in lines:
        match = GPU_IPC_RE.search(line)
        if match:
            commit()
            current = {'ipc': float(match.group(1))}
            continue
        match = TOTAL_R_RE.search(line)
        if match:
            r_total = int(match.group(1))
        match = TOTAL_W_RE.search(line)
        if match:
            w_total = int(match.group(1))
        match = CAUSE_R_RE.search(line)
        if match:
            r_reasons[match.group(1)] = int(match.group(2))
        match = CAUSE_W_RE.search(line)
        if match:
            w_reasons[match.group(1)] = int(match.group(2))
        if mq_size is None or mshr_max_merge is None:
            cache_match = CACHE_LINE_RE.search(line)
            if cache_match:
                payload = cache_match.group(1)
                segments = [segment.strip() for segment in payload.split(',')]
                if len(segments) >= 4:
                    mshr_nums = re.findall(r"\d+", segments[2])
                    mq_nums = re.findall(r"\d+", segments[3])
                    if mshr_nums:
                        mshr_max_merge = int(mshr_nums[-1])
                    if mq_nums:
                        mq_size = int(mq_nums[0])

    commit()

    if not records and (r_total or w_total):
        records = [{
            'ipc': None,
            'r_total': r_total,
            'w_total': w_total,
            'r_reasons': dict(r_reasons),
            'w_reasons': dict(w_reasons),
            'mq_size': mq_size,
            'mshr_max_merge': mshr_max_merge,
        }]
    return records


def normalize_cause_label(cause: str) -> str:
    if not cause:
        return cause
    if '][' in cause:
        return cause.split('][', 1)[0]
    return cause


def aggregate_variant_fail_data(records):
    cause_totals = defaultdict(int)
    total_fails = 0
    for record in records:
        for reason_key in ('r_reasons', 'w_reasons'):
            reasons = record.get(reason_key) or {}
            for cause, count in reasons.items():
                try:
                    amount = int(count)
                except (TypeError, ValueError):
                    continue
                if amount <= 0:
                    continue
                normalized = normalize_cause_label(cause)
                cause_totals[normalized] += amount
                total_fails += amount
    ordered = OrderedDict()
    for cause, value in sorted(cause_totals.items(), key=lambda item: (-item[1], item[0])):
        ordered[cause] = value
    return total_fails, ordered


def load_history(path: str):
    rows = []
    if not path or not os.path.exists(path):
        return rows
    try:
        with open(path, 'r', encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows.append(row)
    except OSError:
        return rows
    return rows


def persist_history(path: str, rows):
    if not path:
        return
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fieldnames = ['variant', 'mq', 'mshr_max_merge', 'miss_queue_full', 'target_fail_count', 'top_cause', 'top_cause_count', 'total_fails']
    with open(path, 'w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def maybe_generate_plot(path: str, rows, fine_grained_variants, log_path: str):
    if not path:
        return
    try:
        import matplotlib
        if not os.environ.get('DISPLAY'):
            try:
                matplotlib.use('Agg')
            except RuntimeError:
                pass
        import matplotlib.pyplot as plt
    except ImportError:
        print(f'[WARN] matplotlib not available; skip {TARGET_FAIL_CAUSE} plot generation.')
        return
    except Exception as exc:
        print(f'[WARN] matplotlib backend init failed ({exc!r}); skip {TARGET_FAIL_CAUSE} plot generation.')
        return

    points = []
    for row in rows:
        variant = (row.get('variant') or '').strip()
        mq_raw = (row.get('mq') or '').strip()
        target_raw = ''
        if 'target_fail_count' in row and row['target_fail_count'] is not None:
            target_raw = str(row['target_fail_count']).strip()
        elif 'miss_queue_full' in row and row['miss_queue_full'] is not None:
            target_raw = str(row['miss_queue_full']).strip()
        fails_raw = (row.get('total_fails') or '').strip()
        if not mq_raw:
            continue
        try:
            mq_val = float(mq_raw)
        except (TypeError, ValueError):
            continue
        try:
            target_val = float(target_raw) if target_raw else 0.0
        except (TypeError, ValueError):
            target_val = 0.0
        try:
            fails_val = float(fails_raw) if fails_raw else 0.0
        except (TypeError, ValueError):
            fails_val = 0.0
        if variant.startswith('perf-study-'):
            variant_short = variant[len('perf-study-'):]
        else:
            variant_short = variant
        points.append({
            'variant': variant,
            'variant_short': variant_short,
            'mq': mq_val,
            'mq_int': int(round(mq_val)),
            'target_fail': target_val,
            'total_fails': fails_val,
        })

    if not points:
        print(f'[INFO] no numeric entries available for {TARGET_FAIL_CAUSE} plot.')
        return

    points.sort(key=lambda item: item['mq'])

    fine_grained_set = {name for name in (fine_grained_variants or []) if name}

    standard_points = [item for item in points if item['variant_short'] not in fine_grained_set]
    if not standard_points:
        standard_points = points[:]
    standard_points.sort(key=lambda item: item['mq'])

    fig, (ax_main, ax_secondary, ax_delta) = plt.subplots(1, 3, figsize=(20, 5))

    if standard_points:
        x_vals = [item['mq'] for item in standard_points]
        y_vals = [item['target_fail'] for item in standard_points]
        if len(x_vals) >= 2:
            for idx in range(1, len(x_vals)):
                color = 'tab:blue' if idx == len(x_vals) - 1 else 'black'
                ax_main.plot(
                    [x_vals[idx - 1], x_vals[idx]],
                    [y_vals[idx - 1], y_vals[idx]],
                    color=color,
                    linewidth=1.5,
                )
        ax_main.scatter(x_vals, y_vals, color='black', zorder=3)
        for item in standard_points:
            ax_main.vlines(
                item['mq'],
                0,
                item['target_fail'],
                colors='tab:gray',
                linestyles='dashed',
                linewidth=1.0,
                alpha=0.5,
            )
            ax_main.annotate(
                f"{item['mq_int']}",
                xy=(item['mq'], 0),
                xytext=(0, -12),
                textcoords='offset points',
                ha='center',
                va='top',
                fontsize=8,
                color='tab:gray',
            )
        ax_main.set_xlim(left=x_vals[0])
    else:
        ax_main.text(0.5, 0.5, 'No data for trend plot', transform=ax_main.transAxes, ha='center', va='center')
        ax_main.axis('off')

    ax_main.set_xlabel('<mq> entries')
    ax_main.set_ylabel(f'{TARGET_FAIL_CAUSE} count')
    ax_main.set_title(f'{TARGET_FAIL_CAUSE} vs <mq> trend')
    ax_main.grid(True, linestyle='--', alpha=0.3)
    ax_main.set_ylim(bottom=0)
    ax_main.tick_params(axis='x', labelbottom=False)

    baseline_point = None
    for item in standard_points:
        if item['mq_int'] == 16:
            baseline_point = item
            break
    if baseline_point is None:
        for item in points:
            if item['mq_int'] == 16:
                baseline_point = item
                break
    if baseline_point is None and standard_points:
        baseline_point = standard_points[0]
    if baseline_point is None:
        baseline_point = points[0]

    baseline_mq_int = baseline_point['mq_int']
    baseline_target_fail = baseline_point['target_fail']
    baseline_variant = baseline_point.get('variant', '')

    fine_points = [item for item in points if item['variant_short'] in fine_grained_set]
    fine_points.sort(key=lambda item: item['mq'])

    selected_points = []
    if baseline_point:
        selected_points.append(baseline_point)
    selected_points.extend(fine_points)

    log_lines = []
    log_lines.append(
        f"baseline_variant={baseline_variant} mq={baseline_point['mq']} {TARGET_FAIL_CAUSE.lower()}={baseline_target_fail}"
    )

    if selected_points:
        plotted_points = []
        xticklabels = []
        for idx, point in enumerate(selected_points):
            resource = point['mq'] if point['mq'] else 1.0
            ror = (baseline_target_fail - point['target_fail']) / resource
            log_lines.append(
                f"variant={point.get('variant','')} mq={point['mq']} {TARGET_FAIL_CAUSE.lower()}={point['target_fail']} baseline_ror=( {baseline_target_fail} - {point['target_fail']} ) / {resource} = {ror:.6f}"
            )
            if idx == 0:
                continue
            plotted_points.append((point, ror))
            xticklabels.append(str(point['mq_int']))

        if plotted_points:
            positions = list(range(len(plotted_points)))
            values = [item[1] for item in plotted_points]
            ax_secondary.bar(positions, values, color='tab:blue', alpha=0.8)
            ax_secondary.set_xticks(positions)
            ax_secondary.set_xticklabels(xticklabels)
            for pos, value in enumerate(values):
                if math.isclose(value, 0.0, abs_tol=1e-9):
                    va = 'bottom'
                    offset = 3
                elif value > 0:
                    va = 'bottom'
                    offset = 3
                else:
                    va = 'top'
                    offset = -6
                ax_secondary.annotate(
                    f'ror={value:.2f}',
                    xy=(pos, value),
                    xytext=(0, offset),
                    textcoords='offset points',
                    ha='center',
                    va=va,
                    fontsize=8,
                    color='tab:blue',
                )
        else:
            ax_secondary.text(0.5, 0.5, 'No data for rate-of-return plot', transform=ax_secondary.transAxes, ha='center', va='center')
            ax_secondary.axis('off')
    else:
        ax_secondary.text(0.5, 0.5, 'No data for rate-of-return plot', transform=ax_secondary.transAxes, ha='center', va='center')
        ax_secondary.axis('off')

    ax_secondary.set_xlabel('<mq> entries')
    ax_secondary.set_ylabel('rate of return (ror)')
    ax_secondary.set_title('Rate of return relative to baseline')
    ax_secondary.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax_secondary.axhline(0.0, color='black', linewidth=0.8)

    if selected_points and len(selected_points) >= 2:
        delta_positions = list(range(len(selected_points) - 1))
        delta_values = []
        delta_labels = []
        for idx in range(1, len(selected_points)):
            prev = selected_points[idx - 1]
            curr = selected_points[idx]
            delta_mq = curr['mq'] - prev['mq']
            delta_fails = prev['target_fail'] - curr['target_fail']
            rate = delta_fails / delta_mq if not math.isclose(delta_mq, 0.0) else 0.0
            delta_values.append(rate)
            delta_labels.append(f"{curr['mq_int']}")
            log_lines.append(
                f"delta {prev.get('variant','')}->{curr.get('variant','')}: ( {prev['target_fail']} - {curr['target_fail']} ) / ( {curr['mq']} - {prev['mq']} ) = {rate:.6f}"
            )
        ax_delta.bar(delta_positions, delta_values, color='tab:orange', alpha=0.8)
        ax_delta.set_xticks(delta_positions)
        ax_delta.set_xticklabels(delta_labels)
        for pos, value in enumerate(delta_values):
            if math.isclose(value, 0.0, abs_tol=1e-9):
                va = 'bottom'
                offset = 3
            elif value > 0:
                va = 'bottom'
                offset = 3
            else:
                va = 'top'
                offset = -6
            ax_delta.annotate(
                f'ror={value:.2f}',
                xy=(pos, value),
                xytext=(0, offset),
                textcoords='offset points',
                ha='center',
                va=va,
                fontsize=8,
                color='tab:orange',
            )
    else:
        ax_delta.text(0.5, 0.5, 'No adjacent deltas to report', transform=ax_delta.transAxes, ha='center', va='center')
        ax_delta.axis('off')

    ax_delta.set_xlabel('consecutive <mq> pairs')
    ax_delta.set_ylabel('rate of return (ror)')
    ax_delta.set_title('Adjacent delta ror (Δfails/Δ<mq>)')
    ax_delta.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax_delta.axhline(0.0, color='black', linewidth=0.8)

    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print(f'[INFO] wrote {TARGET_FAIL_CAUSE} plot to {path}')

    if log_path:
        try:
            directory = os.path.dirname(log_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(log_path, 'w', encoding='utf-8') as handle:
                handle.write('\n'.join(log_lines).rstrip() + '\n')
            print(f'[INFO] wrote ROR details to {log_path}')
        except OSError as exc:
            print(f'[WARN] failed to write ROR log {log_path}: {exc!r}')


def main():
    if len(sys.argv) < 9:
        sys.exit('[ERROR] expected sim_root, variant_tag, summary_path, decision_path, history_path, plot_path, log_path, fine_grained_variants, and optional case directories')
    sim_root = sys.argv[1]
    variant_tag = sys.argv[2]
    summary_path = sys.argv[3]
    decision_path = sys.argv[4]
    history_path = sys.argv[5]
    plot_path = sys.argv[6]
    log_path = sys.argv[7]
    fine_grained_csv = sys.argv[8]
    fine_grained_variants = [item.strip() for item in fine_grained_csv.split(',') if item.strip()]
    case_dirs = sys.argv[9:]

    results = []
    overall_cause_totals = defaultdict(int)
    overall_fail_sum = 0
    mq_size = None
    mshr_max_merge = None
    for case_dir in case_dirs:
        rel_path = os.path.relpath(case_dir, sim_root)
        bench_name = rel_path.split(os.sep)[0]
        latest = pick_latest(case_dir)
        if not latest:
            results.append((bench_name, None, None, case_dir))
            continue
        records = parse_log(latest)
        if mq_size is None or mshr_max_merge is None:
            for record in records:
                mq_candidate = record.get('mq_size')
                merge_candidate = record.get('mshr_max_merge')
                if mq_candidate is not None and merge_candidate is not None:
                    mq_size = mq_candidate
                    mshr_max_merge = merge_candidate
                    break
        total_fails, cause_totals = aggregate_variant_fail_data(records)
        results.append((bench_name, total_fails, cause_totals, latest))
        if cause_totals:
            for cause, value in cause_totals.items():
                overall_cause_totals[cause] += value
                overall_fail_sum += value

    lines = []
    lines.append(f'Variant: {variant_tag}')
    lines.append(f'Simulation root: {sim_root}')
    lines.append('')

    overall_entries = []

    if not results:
        lines.append('[WARN] No case directories supplied. Nothing to report.')
    else:
        for bench_name, total_fails, cause_totals, source_file in sorted(results, key=lambda item: item[0]):
            lines.append(f'Benchmark: {bench_name}')
            if total_fails is None or cause_totals is None:
                lines.append('  No .o log found; skip fail breakdown.')
                lines.append('')
                continue
            lines.append(f'  Log source: {source_file}')
            lines.append(f'  Total fails: {total_fails}')
            if total_fails <= 0 or not cause_totals:
                lines.append('  No fail causes recorded.')
                lines.append('')
                continue
            lines.append('  Cause breakdown (sorted by share):')
            for cause, value in cause_totals.items():
                share = (value / total_fails) * 100 if total_fails else 0.0
                lines.append(f'    - {cause}: {value} ({share:.2f}%)')
            lines.append('')

        if overall_cause_totals:
            lines.append('Overall cause totals (all benchmarks):')
            for cause, value in sorted(overall_cause_totals.items(), key=lambda item: (-item[1], item[0])):
                share = (value / overall_fail_sum) * 100 if overall_fail_sum else 0.0
                entry = f'{cause}: {value} ({share:.2f}%)'
                lines.append(f'  - {entry}')
                overall_entries.append(entry)
            lines.append('')

    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as handle:
        handle.write('\n'.join(lines).rstrip() + '\n')

    if overall_entries:
        result_summary = '; '.join(overall_entries)
        decision = 'continue regress'
    else:
        result_summary = 'No fails recorded'
        decision = 'stop regress'

    mq_display = mq_size if mq_size is not None else 'unknown'
    merge_display = mshr_max_merge if mshr_max_merge is not None else 'unknown'
    with open(decision_path, 'a', encoding='utf-8') as handle:
        handle.write(
            f"cfg: {{<max_merge>: {merge_display}, <mq>: {mq_display}}} "
            f'result: "{result_summary}" decision: "{decision}"\n'
        )

    miss_queue_full = overall_cause_totals.get('MISS_QUEUE_FULL', 0)
    target_fail_count = overall_cause_totals.get(TARGET_FAIL_CAUSE, 0)
    if overall_cause_totals:
        ordered_overall = sorted(overall_cause_totals.items(), key=lambda item: (-item[1], item[0]))
        top_cause, top_cause_count = ordered_overall[0]
    else:
        top_cause, top_cause_count = '', 0

    if mq_size is None:
        print(f"[WARN] variant {variant_tag} produced no mq_size; skip history update to preserve existing data.")
        history_rows = load_history(history_path)
        if history_rows:
            maybe_generate_plot(plot_path, history_rows, fine_grained_variants, log_path)
        return

    history_rows = load_history(history_path)
    row_map = {row.get('variant'): row for row in history_rows if row.get('variant')}
    row_map[variant_tag] = {
        'variant': variant_tag,
        'mq': str(mq_size),
        'mshr_max_merge': str(mshr_max_merge) if mshr_max_merge is not None else '',
        'miss_queue_full': str(int(miss_queue_full)) if miss_queue_full is not None else '0',
        'target_fail_count': str(int(target_fail_count)) if target_fail_count is not None else '0',
        'top_cause': top_cause,
        'top_cause_count': str(int(top_cause_count)) if top_cause_count else '0',
        'total_fails': str(int(overall_fail_sum)) if overall_fail_sum else '0',
    }
    updated_rows = [row_map[key] for key in sorted(row_map)]
    persist_history(history_path, updated_rows)
    maybe_generate_plot(plot_path, updated_rows, fine_grained_variants, log_path)


if __name__ == '__main__':
    main()
PY
    echo "[INFO] wrote fail cause summary to $summary_file"
done
