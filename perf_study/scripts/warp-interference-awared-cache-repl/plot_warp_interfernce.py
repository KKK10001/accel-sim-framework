import matplotlib
# Handle headless environments
matplotlib.use('Agg')  # Use non-interactive backend to avoid GTK errors

import matplotlib.pyplot as plt
import numpy as np
import re
import os
import glob
from matplotlib.colors import Normalize
import matplotlib.patches as mpatches

# Font settings
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def compute_interference_stats(interference_dict, trim_ratio=0.10):
    """
    Compute robust statistics on non-zero interference values.
    Uses trimmed mean to reduce the impact of outliers.
    """
    values = np.array(list(interference_dict.values()), dtype=float)
    if values.size == 0:
        return {
            'mean': 0.0,
            'trimmed_mean': 0.0,
            'std': 0.0,
            'max': 0.0,
            'count': 0,
        }

    sorted_vals = np.sort(values)
    trim_k = int(values.size * trim_ratio)
    if trim_k > 0 and (2 * trim_k) < values.size:
        trimmed = sorted_vals[trim_k: values.size - trim_k]
    else:
        trimmed = sorted_vals

    return {
        'mean': float(np.mean(values)),
        'trimmed_mean': float(np.mean(trimmed)),
        'std': float(np.std(values)),
        'max': float(np.max(values)),
        'count': int(values.size),
    }

def parse_interference_file(filename):
    """
    Parse interference file and return interference matrix data and all involved warps.
    Format: warp_interfere[sid:X][warp:interfered][warp:interfering] = value
    """
    interference_dict = {}
    all_warps = set()
    
    with open(filename, 'r') as f:
        for line in f:
            # Parse with regular expression
            pattern = r'warp_interfere\[sid:\d+\]\[warp:(\d+)\]\[warp:(\d+)\]\s*=\s*(\d+)'
            match = re.search(pattern, line)
            
            if match:
                interfered = int(match.group(1))  # Interfered warp (y-axis)
                interfering = int(match.group(2))  # Interfering warp (x-axis)
                value = int(match.group(3))
                
                interference_dict[(interfered, interfering)] = value
                all_warps.add(interfered)
                all_warps.add(interfering)
    
    return interference_dict, sorted(all_warps)


def compute_n_interfered(interference_dict):
    """
    For each interfered warp y, count number of distinct interfering warps z.
        Returns:
            - n_interfered_map: {y: count(distinct z)}
            - n_interfered_warps: number of unique interfered warps y (no duplicate counting)
            - total_interference: sum of all interference values (last column)
    """
    interfered_to_interfering = {}
    total_interference = 0

    for (interfered, interfering), value in interference_dict.items():
        if interfered not in interfered_to_interfering:
            interfered_to_interfering[interfered] = set()
        interfered_to_interfering[interfered].add(interfering)
        total_interference += value

    n_interfered_map = {
        interfered: len(interfering_set)
        for interfered, interfering_set in interfered_to_interfering.items()
    }
    n_interfered_warps = int(len(n_interfered_map))
    return n_interfered_map, n_interfered_warps, int(total_interference)


def compute_max_entry(interference_dict):
    """
    Return one max entry in the form (interfered_warp, interfering_warp, value).
    If there are multiple with same max, the first encountered is returned.
    """
    if not interference_dict:
        return None

    max_pair = None
    max_value = -1
    for (interfered, interfering), value in interference_dict.items():
        if value > max_value:
            max_value = value
            max_pair = (interfered, interfering, value)
    return max_pair

def create_heatmap(interference_dict, warps, sid, output_dir='.'):
    """
    Create heatmap.
    """
    if not warps:
        print(f"sid_{sid} has no data")
        return
    
    n = len(warps)
    # Create warp-to-index mapping
    warp_to_idx = {warp: i for i, warp in enumerate(warps)}
    
    # Initialize matrix
    matrix = np.zeros((n, n))
    
    # Fill matrix
    max_value = 0
    for (interfered, interfering), value in interference_dict.items():
        if interfered in warp_to_idx and interfering in warp_to_idx:
            i = warp_to_idx[interfered]
            j = warp_to_idx[interfering]
            matrix[i, j] = value
            max_value = max(max_value, value)

    stats = compute_interference_stats(interference_dict)
    n_interfered_map, n_interfered_warps, total_interference = compute_n_interfered(interference_dict)
    max_entry = compute_max_entry(interference_dict)
    
    # Normalize to [0, 1]
    if max_value > 0:
        matrix_normalized = matrix / max_value
    else:
        matrix_normalized = matrix
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Draw heatmap
    im = ax.imshow(matrix_normalized, cmap='YlOrRd', aspect='auto', 
                   vmin=0, vmax=1, interpolation='nearest')
    
    # Set axes
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels([f'W{warp}' for warp in warps], rotation=90, fontsize=8)
    ax.set_yticklabels([f'W{warp}' for warp in warps], fontsize=8)
    
    # Set labels
    ax.set_xlabel('Interfering Warp', fontsize=12)
    ax.set_ylabel('Interfered Warp', fontsize=12)
    if max_entry is not None:
        max_line = (
            f'warp_interfere[sid:{sid}][warp:{max_entry[0]}][warp:{max_entry[1]}] '
            f'= max = {int(max_entry[2])}'
        )
    else:
        max_line = f'warp_interfere[sid:{sid}][warp:-][warp:-] = max = 0'

    ax.set_title(
        f'SID {sid}: n_interfered = {n_interfered_warps}, total_interference = {total_interference}\n'
        f'raw mean = {stats["mean"]:.2f}, '
        f'trimmed mean(10%) = {stats["trimmed_mean"]:.2f}, '
        f'SD (Std. Dev.) = {stats["std"]:.2f}\n'
        f'{max_line}',
        fontsize=10
    )
    
    # Add color bar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Normalized Interference Value', fontsize=10)
    
    # Show cell values (optional, only for small matrices)
    if n <= 20:
        for i in range(n):
            for j in range(n):
                if matrix[i, j] > 0:
                    text_color = 'white' if matrix_normalized[i, j] > 0.5 else 'black'
                    ax.text(j, i, f'{int(matrix[i, j])}', 
                           ha='center', va='center', color=text_color, fontsize=6)
    
    plt.tight_layout()
    
    # Save figure
    output_file = os.path.join(output_dir, f'sid_{sid}_interference_heatmap.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Generated: {output_file}")
    print(
        f"  - avg interference = {stats['trimmed_mean']:.2f}, "
        f"SD (Std. Dev.) = {stats['std']:.2f}, "
        f"max interference = {max_value}, "
        f"n_interfered = {n_interfered_warps}, total interference = {total_interference}"
    )
    if max_entry is not None:
        print(
            f"  - max sample: warp_interfere[sid:{sid}][warp:{max_entry[0]}][warp:{max_entry[1]}] "
            f"= max = {int(max_entry[2])}"
        )
    print(
        f"  - raw mean = {stats['mean']:.2f}, trimmed-mean(10%) = {stats['trimmed_mean']:.2f}, "
        f"samples = {stats['count']}"
    )
    if n_interfered_map:
        avg_n_interfered = float(np.mean(list(n_interfered_map.values())))
        max_n_interfered = int(max(n_interfered_map.values()))
    else:
        avg_n_interfered = 0.0
        max_n_interfered = 0
    print(
        f"  - n_interfered: {len(n_interfered_map)} interfered warps, "
        f"avg distinct interferers = {avg_n_interfered:.2f}, "
        f"max distinct interferers = {max_n_interfered}"
    )

    # Save n_interfered details per SID
    n_interfered_file = os.path.join(output_dir, f'sid_{sid}_n_interfered.txt')
    with open(n_interfered_file, 'w') as fout:
        fout.write('interfered_warp,n_interfered\n')
        for interfered, count in sorted(n_interfered_map.items(), key=lambda x: (-x[1], x[0])):
            fout.write(f'{interfered},{count}\n')
    print(f"  - n_interfered detail saved: {n_interfered_file}")
    print(f"  - Involved warps ({n}): {warps}")
    
    return (
        matrix,
        warps,
        max_value,
        n_interfered_warps,
        total_interference,
        stats['mean'],
        stats['trimmed_mean'],
        stats['std'],
        -1 if max_entry is None else int(max_entry[0]),
        -1 if max_entry is None else int(max_entry[1]),
    )

def process_all_sid_files(file_pattern='sid_*_warp_interfere*.txt'):
    """
    Process all SID files matching the pattern.
    """
    sid_files = glob.glob(file_pattern)
    if not sid_files:
        print(f"No files matched pattern: {file_pattern}")
        print("Current directory:", os.getcwd())
        print("Directory listing:", os.listdir('.'))
        return
    
    print(f"Found {len(sid_files)} SID files: {sid_files}")
    
    for file in sid_files:
        # Extract SID from file name
        match = re.search(r'sid_(\d+)_warp_interfere(?:nce)?\.txt', file)
        if match:
            sid = int(match.group(1))
            print(f"\nProcessing SID {sid}...")
            
            # Parse file
            interference_dict, warps = parse_interference_file(file)
            
            # Generate heatmap
            create_heatmap(interference_dict, warps, sid)

def create_summary_heatmap(all_data, output_dir='.'):
    """
    Create summary heatmap across all SIDs (one subplot per SID).
    """
    n_sids = len(all_data)
    if n_sids == 0:
        return

    # Fixed 2x2 layout
    rows, cols = 2, 2
    fig, axes = plt.subplots(rows, cols, figsize=(12, 9))
    axes = axes.flatten()

    # Keep deterministic order and cap at 4 SIDs for 2x2
    sid_items = sorted(all_data.items(), key=lambda x: x[0])
    if len(sid_items) > 4:
        print(f"Warning: {len(sid_items)} SIDs found, only first 4 are shown in 2x2 summary.")
    sid_items = sid_items[:4]

    last_im = None

    for idx, (sid, (matrix, warps, max_val, n_interfered_warps, total_interference,
                    raw_mean_interference, trimmed_mean_interference,
                    std_interference, max_interfered_warp,
                    max_interfering_warp)) in enumerate(sid_items):
        ax = axes[idx]
        
        # Normalized display
        if max_val > 0:
            matrix_norm = matrix / max_val
        else:
            matrix_norm = matrix
        
        im = ax.imshow(matrix_norm, cmap='YlOrRd', aspect='auto', 
                       vmin=0, vmax=1, interpolation='nearest')
        last_im = im
        
        ax.set_title(
            f'SID {sid}\n'
            f'n_interfered={n_interfered_warps}, total_interference={total_interference}\n'
            f'raw={raw_mean_interference:.2f}, trim10={trimmed_mean_interference:.2f}, '
            f'SD={std_interference:.2f}\n'
            f'warp_interfere[sid:{sid}][warp:{max_interfered_warp}][warp:{max_interfering_warp}] '
            f'= max = {int(max_val)}',
            fontsize=9
        )
        ax.set_xlabel('Interfering')
        ax.set_ylabel('Interfered')
        
        # Show partial ticks only
        if len(warps) > 10:
            step = max(1, len(warps) // 5)
            ax.set_xticks(np.arange(0, len(warps), step))
            ax.set_yticks(np.arange(0, len(warps), step))
            ax.set_xticklabels([f'W{warps[i]}' for i in range(0, len(warps), step)])
            ax.set_yticklabels([f'W{warps[i]}' for i in range(0, len(warps), step)])
    
    # Hide unused subplots
    for idx in range(len(sid_items), len(axes)):
        axes[idx].axis('off')

    # Shared colorbar on the right (same normalized scale as single-SID heatmaps)
    if last_im is not None:
        cbar_ax = fig.add_axes([0.93, 0.15, 0.015, 0.7])
        cbar = fig.colorbar(last_im, cax=cbar_ax)
        cbar.set_label('Normalized Interference Value', fontsize=10)
    
    plt.suptitle('Warp Interference Summary', fontsize=14)
    plt.tight_layout(rect=[0, 0, 0.91, 0.95])
    
    output_file = os.path.join(output_dir, 'all_sids_interference_summary.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\nGenerated summary figure: {output_file}")

# Main
if __name__ == "__main__":
    print("Start processing warp interference data...")
    print("Current working directory:", os.getcwd())
    # Process all SID files
    process_all_sid_files()
    
    # Optional: create summary figure
    # Collect all data first
    all_data = {}
    sid_files = glob.glob('sid_*_warp_interfere*.txt')
    
    for file in sid_files:
        match = re.search(r'sid_(\d+)_warp_interfere(?:nce)?\.txt', file)
        if match:
            sid = int(match.group(1))
            interference_dict, warps = parse_interference_file(file)
            
            if warps:
                n = len(warps)
                warp_to_idx = {w: i for i, w in enumerate(warps)}
                matrix = np.zeros((n, n))
                max_val = 0
                
                for (interfered, interfering), val in interference_dict.items():
                    if interfered in warp_to_idx and interfering in warp_to_idx:
                        matrix[warp_to_idx[interfered], warp_to_idx[interfering]] = val
                        max_val = max(max_val, val)
                
                stats = compute_interference_stats(interference_dict)
                _n_interfered_map, n_interfered_warps, total_interference = compute_n_interfered(interference_dict)
                max_entry = compute_max_entry(interference_dict)
                all_data[sid] = (
                    matrix,
                    warps,
                    max_val,
                    n_interfered_warps,
                    total_interference,
                    stats['mean'],
                    stats['trimmed_mean'],
                    stats['std'],
                    -1 if max_entry is None else int(max_entry[0]),
                    -1 if max_entry is None else int(max_entry[1]),
                )
    
    if all_data:
        create_summary_heatmap(all_data)
    else:
        print("No sid_*_warp_interfere*.txt data found for summary; all_sids_interference_summary.png was not generated")
    
    print("\nAll heatmaps are generated!")