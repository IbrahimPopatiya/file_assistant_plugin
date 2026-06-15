import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from config import WATCHED_DIR
from database import init_db, insert_event
from event_logger import log_file_event


class FileActivityHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory: return
        print("📌 on_created triggered")
        time.sleep(2)
        
        log_file_event("created", event.src_path,source="File Watcher")
        

    def on_modified(self, event):
        if event.is_directory: return
        print("📌 on_modified triggered")
        log_file_event(event.event_type, event.src_path,source="File Watcher")

    def on_deleted(self, event):
        if event.is_directory: return
        print("📌 on_deleted triggered")
        log_file_event(event.event_type, event.src_path,source="File Watcher")

    def on_moved(self, event):
        if not event.is_directory:
            print("📌 on_moved triggered")
            print("    🔁 From:", event.src_path)
            print("    ✅ To:", event.dest_path)
            log_file_event(event.event_type, event.dest_path,source="File Watcher")


    



def start_watcher(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    init_db()

    event_handler = FileActivityHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)

    print(f"📡 Watching directory: {folder_path}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping watcher...")
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_watcher(WATCHED_DIR)
