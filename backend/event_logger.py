# backend/utils/event_logger.py

import os
from datetime import datetime
from database import insert_event

def log_file_event(event_type, file_path, source="Unknown",extra=None):
    file_path = os.path.abspath(file_path)
    file_name = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

    if event_type == "moved" and extra and "from" in extra:
        print(f"✏️ [{source}] RENAMED - {os.path.basename(extra['from'])} ➡️ {file_name} ({file_size} bytes)")
    else:
        print(f"🧾 [{source}] {event_type.upper()} - {file_name} ({file_size} bytes) - {file_path}")
    insert_event(event_type, file_path, file_name, timestamp, file_size)
