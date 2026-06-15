import sqlite3
import os
from datetime import datetime, timedelta
from ..backend.config import DB_PATH

# def fetch_and_clean_events():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT event_type, file_path, file_name, timestamp, file_size FROM file_events ORDER BY timestamp DESC")
#     events = cursor.fetchall()
#     conn.close()
#     # Only keep the latest event for each file_path
#     final_events = {}
#     for event in events:
#         event_type, file_path, file_name, timestamp, file_size = event
#         if file_path not in final_events:
#             final_events[file_path] = event
#     return list(final_events.values())

def fetch_and_clean_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT event_type, file_path, file_name, timestamp, file_size
        FROM file_events
        ORDER BY timestamp DESC
    """)
    events = cursor.fetchall()
    conn.close()

    # Only keep the latest event for each file_path
    final_events = {}
    for event in events:
        event_type, file_path, file_name, timestamp, file_size = event
        if file_path not in final_events:
            final_events[file_path] = event

    return list(final_events.values())

def filter_temp_files(events):
    # Filter out default/temporary names
    return [
        event for event in events
        if not event[2].startswith("New Text Document")
    ]

def group_events_by_date(events):
    grouped = {}
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    for event in events:
        event_date = datetime.strptime(event[3], "%Y-%m-%d %H:%M:%S").date()
        if event_date == today:
            grouped.setdefault("Today", []).append(event)
        elif event_date == yesterday:
            grouped.setdefault("Yesterday", []).append(event)
        else:
            grouped.setdefault(str(event_date), []).append(event)
    return grouped

def build_context_string(events):
    context = ""
    for event in events:
        event_type, file_path, file_name, timestamp, file_size = event
        context += f"- File_name: {file_name}\n  Directory: {os.path.dirname(file_path)}\n  Event Type: {event_type}\n  Time: {timestamp}\n\n"
    return context 