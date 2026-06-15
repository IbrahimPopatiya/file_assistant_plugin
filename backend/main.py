# backend/main.py
import os
import sys
import atexit
from database import init_db
from active_folder_watcher import ExplorerWatcher

# --- Lock File Logic ---
# Create a lock file to prevent multiple instances of the watcher from running.
# The lock file is placed in the same directory as the script.
lock_file_path = os.path.join(os.path.dirname(__file__), 'watcher.lock')

if os.path.exists(lock_file_path):
    # If the lock file exists, another instance is already running. Exit silently.
    sys.exit(0)

# Create the lock file.
with open(lock_file_path, 'w') as f:
    f.write(str(os.getpid()))

# Register a cleanup function to remove the lock file when the script exits.
def cleanup_lock_file():
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)

atexit.register(cleanup_lock_file)
# --- End of Lock File Logic ---


if __name__ == "__main__":
    print("🚀 Starting File Explorer Watcher...")
    init_db()
    

    watcher = ExplorerWatcher()
    watcher.watch_active_folder()


