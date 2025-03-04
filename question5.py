import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Process scheduling data (Process ID, Start Time, Execution Time, Assigned Processor)
schedule = [
    ("P1", 0, 5, "Processor 1"),  # P1 starts at 0 and runs for 5 units on Processor 1
    ("P2", 3, 1, "Processor 2"),  # P2 starts at 3 and runs for 1 unit on Processor 2
    ("P3", 10, 11, "Processor 1"),  # P3 starts at 10 and runs for 11 units on Processor 1
    ("P4", 12, 5, "Processor 2"),  # P4 starts at 12 and runs for 5 units on Processor 2
    ("P5", 15, 12, "Processor 3")   # P5 starts at 15 and runs for 12 units on Processor 3
]

# Colors for each process
colors = {
    "P1": "red",
    "P2": "blue",
    "P3": "green",
    "P4": "orange",
    "P5": "purple"
}

fig, ax = plt.subplots(figsize=(10, 5))

# Create Gantt chart
for process, start, duration, processor in schedule:
    processor_id = int(processor[-1])  # Extract processor number
    ax.broken_barh([(start, duration)], (processor_id - 0.4, 0.8), color=colors[process], label=process)

# Labels and aesthetics
ax.set_xlabel("Time Units")
ax.set_ylabel("Processors")
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["Processor 1", "Processor 2", "Processor 3"])
ax.set_xticks(range(0, 30, 2))
ax.set_title("Multiprocessing System with 3 Processors")

# Add a legend (avoid duplicates)
handles = [mpatches.Patch(color=colors[p], label=p) for p in colors]
ax.legend(handles=handles, loc="upper right")

# Add watermark
fig.text(0.5, 0.5, "2114061", fontsize=40, color='gray', ha='center', va='center', alpha=0.5, rotation=30)

plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
