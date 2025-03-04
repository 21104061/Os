import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def sjf_non_preemptive_schedule(processes):
    """
    Implements Non-Preemptive Shortest Job First (SJF) Scheduling.
    Returns a list of timeline segments with start and end times.
    """
    # Sort processes by arrival time initially
    processes_sorted = sorted(processes, key=lambda x: x['arrival'])
    
    timeline = []
    ready_queue = []  # Stores available processes
    current_time = 0
    completed_processes = set()

    while len(completed_processes) < len(processes):
        # Add newly arrived processes to ready queue
        for p in processes_sorted:
            if p['id'] not in completed_processes and p['arrival'] <= current_time:
                if p not in ready_queue:
                    ready_queue.append(p)
        
        # If no process is ready, CPU remains idle
        if not ready_queue:
            next_arrival = min(p['arrival'] for p in processes_sorted if p['id'] not in completed_processes)
            timeline.append({"id": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            continue

        # Choose the process with the shortest burst time
        ready_queue.sort(key=lambda x: x['burst'])
        shortest_process = ready_queue.pop(0)
        
        # Run the selected process
        start_time = current_time
        end_time = start_time + shortest_process['burst']
        timeline.append({"id": shortest_process['id'], "start": start_time, "end": end_time})
        
        # Update time and mark process as completed
        current_time = end_time
        completed_processes.add(shortest_process['id'])
    
    return timeline

def plot_gantt(timeline, title="SJF Non-Preemptive Scheduling"):
    """
    Plots a single-row Gantt chart of the timeline.
    """
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
    process_ids = set(seg['id'] for seg in timeline if seg['id'] != 'Idle')

    for seg in timeline:
        start, end, pid = seg['start'], seg['end'], seg['id']
        ax.barh(y_position, width=(end - start), left=start, height=0.4, color=color_map.get(pid, 'black'), edgecolor='black')
        if pid != 'Idle':
            ax.text((start + end)/2, y_position, pid, va='center', ha='center', color='white', fontweight='bold')

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
    processes = [
        {"id": "P1", "arrival": 0,  "burst": 5},
        {"id": "P2", "arrival": 3,  "burst": 1},
        {"id": "P3", "arrival": 10, "burst": 11},
        {"id": "P4", "arrival": 12, "burst": 5},
        {"id": "P5", "arrival": 15, "burst": 12}
    ]
    
    sjf_timeline = sjf_non_preemptive_schedule(processes)
    plot_gantt(sjf_timeline, title="2) Multiprogramming with Shortest Job First (Non-Preemptive)")
