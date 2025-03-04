import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def sjf_preemptive_schedule(processes):
    """
    Implements Preemptive Shortest Job First (SJF) Scheduling (Shortest Remaining Time First).
    Returns a list of timeline segments, where each segment is a dict with keys:
    'id' (process identifier), 'start' (start time), and 'end' (end time).
    """
    # Initialize remaining burst times for each process
    remaining = {p['id']: p['burst'] for p in processes}
    time = 0
    timeline = []
    current_process = None
    segment_start = 0
    completed = set()
    n = len(processes)
    
    # Sort processes by arrival time
    processes_sorted = sorted(processes, key=lambda x: x['arrival'])
    
    # Run simulation until all processes are completed
    while len(completed) < n:
        # List processes that have arrived and are not complete
        available = [p for p in processes_sorted if p['arrival'] <= time and p['id'] not in completed]
        
        if not available:
            # If no process is available, the CPU is idle.
            if current_process != "Idle":
                if current_process is not None:
                    timeline.append({"id": current_process, "start": segment_start, "end": time})
                current_process = "Idle"
                segment_start = time
            time += 1
            continue
        
        # Choose the process with the smallest remaining burst time among those available
        next_proc = min(available, key=lambda x: remaining[x['id']])
        
        # If switching to a new process, record the previous segment
        if current_process != next_proc['id']:
            if current_process is not None:
                timeline.append({"id": current_process, "start": segment_start, "end": time})
            current_process = next_proc['id']
            segment_start = time
        
        # Execute the chosen process for one time unit
        remaining[next_proc['id']] -= 1
        time += 1
        
        # If the process finishes, record its segment and mark it as complete
        if remaining[next_proc['id']] == 0:
            timeline.append({"id": current_process, "start": segment_start, "end": time})
            completed.add(next_proc['id'])
            current_process = None
            segment_start = time

    return timeline

def plot_gantt(timeline, title="Preemptive SJF Scheduling (SRTF)"):
    """
    Plots a single-row Gantt chart for the given timeline.
    Each segment is represented as a horizontal bar with color coding.
    """
    # Define color mapping for processes (and idle time)
    color_map = {
        'P1': 'tab:blue',
        'P2': 'tab:orange',
        'P3': 'tab:green',
        'P4': 'tab:red',
        'P5': 'tab:purple',
        'Idle': 'gray'
    }
    
    fig, ax = plt.subplots(figsize=(10, 3))
    y_position = 0
    
    # Build a set of process IDs (excluding Idle) for legend creation
    process_ids = set(seg['id'] for seg in timeline if seg['id'] != "Idle")
    
    # Plot each segment as a horizontal bar
    for seg in timeline:
        start, end, pid = seg['start'], seg['end'], seg['id']
        ax.barh(y_position, width=(end - start), left=start, height=0.4,
                color=color_map.get(pid, 'black'), edgecolor='black')
        # Label non-idle segments with process ID
        if pid != "Idle":
            ax.text((start + end) / 2, y_position, pid, va='center', ha='center',
                    color='white', fontweight='bold')
    
    # Create legend patches for processes
    legend_patches = [mpatches.Patch(color=color_map[pid], label=pid) for pid in process_ids]
    ax.legend(handles=legend_patches, loc='upper right')
    
    ax.set_title(title)
    ax.set_xlabel("Time (minutes after 5:30 PM)")
    ax.set_ylabel("CPU")
    ax.set_xlim(0, max(seg['end'] for seg in timeline) + 1)
    ax.set_yticks([])
    
    # Add watermark
    fig.text(0.5, 0.5, '2114061', fontsize=40, color='gray', ha='center', va='center', alpha=0.5, rotation=30)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Define processes: arrival time and burst time (in minutes after 5:30 PM)
    processes = [
        {"id": "P1", "arrival": 0,  "burst": 5},
        {"id": "P2", "arrival": 3,  "burst": 1},
        {"id": "P3", "arrival": 10, "burst": 11},
        {"id": "P4", "arrival": 12, "burst": 5},
        {"id": "P5", "arrival": 15, "burst": 12}
    ]
    
    # Generate the preemptive SJF schedule timeline
    sjf_preemptive_timeline = sjf_preemptive_schedule(processes)
    
    # Plot the Gantt chart
    plot_gantt(sjf_preemptive_timeline, title="3) Preemptive SJF Scheduling (SRTF)")
