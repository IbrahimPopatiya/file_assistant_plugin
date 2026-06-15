import sqlite3
import database
from config import DB_FILE
from datetime import datetime, timedelta

def fetch_all_events():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT event_type, file_path, file_name, timestamp, file_size FROM file_events")
    rows = cursor.fetchall()
    
    conn.close()
    return rows




def group_events_by_date(events):
    grouped = {
        "Today": [],
        "Yesterday": [],
        "Last 7 Days": []
    }
    
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)

    for event in events:
        event_type, file_path, file_name, timestamp,  file_size = event
        
        # Convert string timestamp to datetime object
        try:
            event_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue  # Skip malformed entries

        event_date = event_dt.date()

        # Determine the category
        if event_date == today:
            grouped["Today"].append({
                "event_type": event_type,
                "file_path": file_path,
                "timestamp": timestamp,
                "file_name": file_name,
                "file_size": file_size
            })
        elif event_date == yesterday:
            grouped["Yesterday"].append({
                "event_type": event_type,
                "file_path": file_path,
                "timestamp": timestamp,
                "file_name": file_name,
                "file_size": file_size
            })
        elif last_week <= event_date < yesterday:
            grouped["Last 7 Days"].append({
                "event_type": event_type,
                "file_path": file_path,
                "timestamp": timestamp,
                "file_name": file_name,
                "file_size": file_size
            })

    return grouped
