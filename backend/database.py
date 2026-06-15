import sqlite3
from config import DB_FILE
import os 




def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            file_size INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_event(event_type, file_path,file_name, timestamp,file_size):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO file_events (event_type, file_path,file_name, timestamp,file_size)
        VALUES (?, ?, ?,?,?)
    """, (event_type, file_path,file_name, timestamp,file_size))
    conn.commit()
    conn.close()
