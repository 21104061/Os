import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def fcfs_schedule(processes):
    """
    Given a list of processes with 'id', 'arrival', and 'burst',
    returns a list of timeline segments:
    [
      {"id": process_id, "start": start_time, "end": end_time},
      ...
    ]
    including idle segments if needed.
    """
    try:
        # Sort processes by arrival time
        processes_sorted = sorted(processes, key=lambda x: x['arrival'])
        
        timeline = []
        current_time = 0
        
        for p in processes_sorted:
            pid = p['id']
            arrival = p['arrival']
            burst = p['burst']
            
            # If CPU is idle before this process arrives
            if current_time < arrival:
                timeline.append({
                    "id": "Idle",
                    "start": current_time,
                    "end": arrival
                })
                current_time = arrival
            
            # Schedule this process
            start_time = current_time
            end_time = start_time + burst
            timeline.append({
                "id": pid,
                "start": start_time,
                "end": end_time
            })
            current_time = end_time
        
        return timeline
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def plot_gantt(timeline, title="FCFS Scheduling (Multiprogramming System)"):
    """
    Plots a single-row Gantt chart of the timeline.
    Each segment is drawn as a horizontal bar from start to end.
    """
    try:
        # Assign a color to each process (including 'Idle' if desired)
        # You can customize colors as you wish
        color_map = {
            'P1': 'tab:blue',
            'P2': 'tab:orange',
            'P3': 'tab:green',
            'P4': 'tab:red',
            'P5': 'tab:purple',
            'Idle': 'gray'
        }
        
        fig, ax = plt.subplots(figsize=(10, 3))
        
        # We will plot everything on y=0 (a single row)
        y_position = 0
        
        # Build a set of processes (excluding Idle) for legend
        process_ids = set([seg['id'] for seg in timeline if seg['id'] != 'Idle'])
        
        for seg in timeline:
            start = seg['start']
            end = seg['end']
            pid = seg['id']
            
            ax.barh(
                y_position,                 # y
                width=(end - start),        # how long the bar extends
                left=start,                 # start position on x-axis
                height=0.4,                 # thickness of the bar
                color=color_map.get(pid, 'black'),
                edgecolor='black'
            )
            
            # Label the segment with the process ID (optional for Idle)
            if pid != 'Idle':
                ax.text(
                    x=(start + end)/2,
                    y=y_position,
                    s=pid,
                    va='center',
                    ha='center',
                    color='white',
                    fontweight='bold'
                )
        
        # Create legend patches for each real process
        legend_patches = []
        for pid in process_ids:
            patch = mpatches.Patch(color=color_map[pid], label=pid)
            legend_patches.append(patch)
        
        ax.legend(handles=legend_patches, loc='upper right')
        
        # Labeling and formatting
        ax.set_title(title)
        ax.set_xlabel("Time (minutes after 5:30 PM)")
        ax.set_ylabel("CPU")
        
        # Set x-axis limits based on the last segment
        max_time = max(seg['end'] for seg in timeline)
        ax.set_xlim(0, max_time + 1)
        
        # Remove y-ticks (since we're using a single row)
        ax.set_yticks([])
        
        # Add watermark
        fig.text(0.5, 0.5, '2114061', fontsize=40, color='gray', ha='center', va='center', alpha=0.5, rotation=30)
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting: {e}")

if __name__ == "__main__":
    # Define the processes
    # Convert the given arrival times to minutes after 5:30 PM
    processes = [
        {"id": "P1", "arrival": 0,  "burst": 5},
        {"id": "P2", "arrival": 3,  "burst": 1},
        {"id": "P3", "arrival": 10, "burst": 11},
        {"id": "P4", "arrival": 12, "burst": 2},
        {"id": "P5", "arrival": 15, "burst": 12}
    ]
    
    # Generate FCFS schedule
    fcfs_timeline = fcfs_schedule(processes)
    
    # Plot the Gantt chart
    plot_gantt(fcfs_timeline, title="1) Multiprogramming System (FCFS)")
