import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define the processes with arrival and burst times.
processes = [
    {"id": "P1", "arrival": 0,  "burst": 5,  "remaining": 5},
    {"id": "P2", "arrival": 3,  "burst": 4,  "remaining": 4},
    {"id": "P3", "arrival": 10, "burst": 11, "remaining": 11},
    {"id": "P4", "arrival": 12, "burst": 5,  "remaining": 5},
    {"id": "P5", "arrival": 15, "burst": 12, "remaining": 12}
]

TIME_QUANTUM = 2    # time slice per round
NUM_PROC = 2        # two processors

# Initialize simulation variables
global_time = 0
ready_queue = []    # list of process indices (or IDs) waiting to run
schedule_events = []  # each event: (process_id, start_time, end_time, processor_index)
finished = set()    # set of process ids that have finished

# Processors: each is a dict with keys:
# "proc": currently assigned process (None if idle)
# "remaining_slice": remaining time in the current quantum
# "event_start": the start time of the current execution segment
processors = [{"proc": None, "remaining_slice": 0, "event_start": None} for _ in range(NUM_PROC)]

# A helper function to add new arrivals into the ready queue.
def add_arrivals(time):
    for proc in processes:
        if proc["arrival"] == time:
            ready_queue.append(proc["id"])

# A helper function to get a process dictionary by its id.
def get_process(pid):
    for proc in processes:
        if proc["id"] == pid:
            return proc
    return None

# Simulation loop: continue until all processes finish.
# We'll simulate until global_time reaches a point where all processes are finished.
while len(finished) < len(processes):
    # Add processes that arrive at this time.
    add_arrivals(global_time)
    
    # For each processor, update its current execution.
    for i in range(NUM_PROC):
        proc_state = processors[i]
        if proc_state["proc"] is not None:
            # Processor is busy; decrement its slice and process's remaining burst.
            proc_state["remaining_slice"] -= 1
            cur_proc = get_process(proc_state["proc"])
            cur_proc["remaining"] -= 1

            # Check if the process finishes at this time step.
            if cur_proc["remaining"] == 0:
                # Record the event ending at global_time + 1.
                schedule_events.append((cur_proc["id"], proc_state["event_start"], global_time + 1, f"Processor {i+1}"))
                finished.add(cur_proc["id"])
                proc_state["proc"] = None
                proc_state["remaining_slice"] = 0
                proc_state["event_start"] = None
            # Otherwise, if the time slice expires.
            elif proc_state["remaining_slice"] == 0:
                # Record the event.
                schedule_events.append((cur_proc["id"], proc_state["event_start"], global_time + 1, f"Processor {i+1}"))
                # Append the process to the ready queue (if not finished).
                ready_queue.append(cur_proc["id"])
                proc_state["proc"] = None
                proc_state["event_start"] = None
        # If processor is idle, we can assign a new process from the ready queue if available.
        if proc_state["proc"] is None:
            if ready_queue:
                next_pid = ready_queue.pop(0)
                # Skip if this process has finished (could be in queue multiple times).
                if next_pid in finished:
                    continue
                proc_state["proc"] = next_pid
                # New time slice is the minimum of TIME_QUANTUM and remaining burst.
                proc = get_process(next_pid)
                proc_state["remaining_slice"] = min(TIME_QUANTUM, proc["remaining"])
                proc_state["event_start"] = global_time
            else:
                # If still idle, record an idle event if not already recording one.
                # We record idle events per processor.
                if proc_state.get("idle") is None:
                    proc_state["idle"] = True
                    proc_state["event_start"] = global_time
        else:
            # Processor busy; mark that it is not idle.
            proc_state["idle"] = False
        # For processors that are idle and remain idle, if they had been idle in the previous time step, 
        # we update nothing here. We'll record idle events when a process is assigned.
        if proc_state["proc"] is None and proc_state.get("idle") and (global_time > proc_state["event_start"]):
            # We record idle events for each time unit while idle.
            schedule_events.append(("Idle", proc_state["event_start"], global_time + 1, f"Processor {i+1}"))
            proc_state["event_start"] = global_time + 1

    global_time += 1

# After simulation, some processors might be idle. We won't extend idle events further.
# Now, use matplotlib to plot the schedule.

# Define colors for processes.
colors = {
    "P1": "tab:blue",
    "P2": "tab:orange",
    "P3": "tab:green",
    "P4": "tab:red",
    "P5": "tab:purple",
    "Idle": "gray"
}

fig, ax = plt.subplots(figsize=(12, 6))

# Plot each schedule event using broken_barh.
for event in schedule_events:
    pid, start, end, proc_label = event
    # Extract processor number from label for vertical positioning.
    proc_num = int(proc_label.split()[-1])
    ax.broken_barh([(start, end - start)], (proc_num - 0.4, 0.8), color=colors.get(pid, "black"), edgecolor="black")
    # Optionally, label non-idle events.
    if pid != "Idle":
        ax.text((start + end) / 2, proc_num, pid, ha="center", va="center", color="white", fontweight="bold")

# Set axes labels and ticks.
ax.set_xlabel("Time Units")
ax.set_ylabel("Processors")
ax.set_yticks([1, 2])
ax.set_yticklabels(["Processor 1", "Processor 2"])
ax.set_title("Multiprocessing Time-Sharing System (2 Processors, Time Slice = 2)")
ax.set_xlim(0, global_time + 1)
ax.grid(True, linestyle="--", alpha=0.6)

# Create legend (avoid duplicates).
legend_handles = [mpatches.Patch(color=colors[p], label=p) for p in colors]
ax.legend(handles=legend_handles, loc="upper right")

# Add watermark.
fig.text(0.5, 0.5, "2114061", fontsize=40, color='gray', ha='center', va='center', alpha=0.5, rotation=30)

plt.tight_layout()
plt.show()
