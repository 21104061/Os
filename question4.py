import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def round_robin_schedule(processes, time_quantum):
    """
    Implements Round Robin Scheduling.
    
    Parameters:
      processes   : List of dictionaries with keys 'id', 'arrival', and 'burst'
      time_quantum: Time quantum for each time slice.
      
    Returns:
      timeline: A list of segments, where each segment is a dict:
                { "id": process_id, "start": start_time, "end": end_time }.
    """
    timeline = []
    current_time = 0
    remaining = {p['id']: p['burst'] for p in processes}
    
    # Sort processes by arrival time.
    processes_sorted = sorted(processes, key=lambda p: p['arrival'])
    n = len(processes)
    ready_queue = []
    i = 0  # pointer to track new arrivals
    
    # Add processes that have already arrived at time 0.
    while i < n and processes_sorted[i]['arrival'] <= current_time:
        ready_queue.append(processes_sorted[i])
        i += 1
        
    while ready_queue or i < n:
        if not ready_queue:
            # CPU idle until the next process arrives.
            next_arrival = processes_sorted[i]['arrival']
            timeline.append({"id": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            while i < n and processes_sorted[i]['arrival'] <= current_time:
                ready_queue.append(processes_sorted[i])
                i += 1
        else:
            proc = ready_queue.pop(0)
            pid = proc['id']
            exec_time = min(time_quantum, remaining[pid])
            start_time = current_time
            end_time = current_time + exec_time
            timeline.append({"id": pid, "start": start_time, "end": end_time})
            current_time = end_time
            remaining[pid] -= exec_time
            
            # Add any processes that have arrived during this time slice.
            while i < n and processes_sorted[i]['arrival'] <= current_time:
                ready_queue.append(processes_sorted[i])
                i += 1
            
            # If the process is not finished, re-add it to the end of the queue.
            if remaining[pid] > 0:
                ready_queue.append(proc)
                
    return timeline

def plot_gantt(timeline, title="Round Robin Scheduling"):
    """
    Plots a single-row Gantt chart for the given timeline.
    Each segment is drawn as a horizontal bar with color coding.
    A watermark "21104061" is added to the plot.
    """
    # Define color mapping for processes and idle time.
    color_map = {
        'P1': 'tab:blue',
        'P2': 'tab:orange',
        'P3': 'tab:green',
        'P4': 'tab:red',
        'P5': 'tab:purple',
        'Idle': 'gray'
    }
    
    fig, ax = plt.subplots(figsize=(12, 3))
    y_position = 0  # single row
    
    for seg in timeline:
        start, end, pid = seg['start'], seg['end'], seg['id']
        ax.barh(
            y_position,
            width=(end - start),
            left=start,
            height=0.4,
            color=color_map.get(pid, 'black'),
            edgecolor='black'
        )
        if pid != "Idle":
            ax.text((start + end) / 2, y_position, pid,
                    va='center', ha='center', color='white', fontweight='bold')
    
    # Add watermark "21104061" to the center of the plot.
    ax.text(0.5, 0.5, "21104061", transform=ax.transAxes,
            fontsize=40, color='gray', alpha=0.3, ha='center', va='center', rotation=30)
    
    # Create legend patches for processes (excluding Idle).
    process_ids = set(seg['id'] for seg in timeline if seg['id'] != "Idle")
    legend_patches = [mpatches.Patch(color=color_map[pid], label=pid) for pid in process_ids]
    ax.legend(handles=legend_patches, loc='upper right')
    
    ax.set_title(title)
    ax.set_xlabel("Time (units)")
    ax.set_ylabel("CPU")
    ax.set_xlim(0, max(seg['end'] for seg in timeline) + 1)
    ax.set_yticks([])
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Define processes with arrival and burst times.
    processes = [
        {"id": "P1", "arrival": 0,  "burst": 5},
        {"id": "P2", "arrival": 3,  "burst": 1},
        {"id": "P3", "arrival": 10, "burst": 11},
        {"id": "P4", "arrival": 12, "burst": 5},
        {"id": "P5", "arrival": 15, "burst": 12}
    ]
    
    # Set the correct time quantum for Round Robin Scheduling.
    time_quantum = 2
    
    # Generate the Round Robin schedule timeline.
    rr_timeline = round_robin_schedule(processes, time_quantum)
    
    # Plot the Gantt chart with watermark.
    plot_gantt(rr_timeline, title="4) Time sharing (Time Quantum = {})".format(time_quantum))
