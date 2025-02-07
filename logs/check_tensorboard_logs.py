from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import os

log_dir = "D:/final year project/project folder/Final-year-full-sem/logs"
event_file = None

# Find the event file
for file in os.listdir(log_dir):
    if "events.out.tfevents" in file:
        event_file = os.path.join(log_dir, file)
        break

if event_file:
    print(f"[INFO] Found event file: {event_file}")
    event_acc = EventAccumulator(event_file)
    event_acc.Reload()

    # Check for scalars
    print("[INFO] Available Tags in TensorBoard Logs:")
    print(event_acc.Tags())

    # Check if rollout/ep_rew_mean exists
    if "rollout/ep_rew_mean" in event_acc.Tags().get("scalars", []):
        scalar_data = event_acc.Scalars("rollout/ep_rew_mean")
        print("[INFO] Found scalar values for 'rollout/ep_rew_mean'")
        print(scalar_data)
    else:
        print("[WARNING] 'rollout/ep_rew_mean' not found in logs.")
else:
    print("[ERROR] No event file found in logs directory.")
