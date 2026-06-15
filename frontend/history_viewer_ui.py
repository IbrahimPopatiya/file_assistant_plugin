import tkinter as tk
import os
import sys

# Create a robust, absolute path to the backend directory
# This ensures modules can be found regardless of how the script is launched
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

from utils import fetch_and_clean_events, filter_temp_files, group_events_by_date

# Use absolute path to ensure it works when launched from context menu
from backend.config import DB_PATH

root = tk.Tk()
root.title("File Assistant - History Viewer")
root.geometry("400x400")

tk.Label(root, text="File History", font=("Arial", 14)).pack(pady=5)

# Fetch, clean, and group events
all_events = fetch_and_clean_events()
filtered_events = filter_temp_files(all_events)
grouped = group_events_by_date(filtered_events)

def on_file_click(path):
    os.startfile(os.path.dirname(path))

# Show groups in order: Today, Yesterday, then by date descending
for group in ["Today", "Yesterday"] + sorted([k for k in grouped if k not in ("Today", "Yesterday")], reverse=True):
    if group in grouped:
        tk.Label(root, text=group, font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        for event in grouped[group]:
            event_type, file_path, file_name, timestamp, file_size = event
            lbl = tk.Label(root, text=file_name, fg="blue", cursor="hand2")
            lbl.pack(anchor="w", padx=30)
            lbl.bind("<Button-1>", lambda e, p=file_path: on_file_click(p))

root.mainloop() 