# backend/active_folder_watcher.py

import time
import os
import logging
from pywinauto import Desktop,Application
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from database import insert_event
import win32com.client
import pythoncom
from event_logger import log_file_event

# --- Start of Logging Setup ---
log_file_path = os.path.join(os.path.dirname(__file__), 'watcher.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# --- End of Logging Setup ---


def get_active_folder():
    try:
        windows = Desktop(backend="uia").windows()
        for w in windows:
            if "File Explorer" in w.window_text():
                try:
                    address_bar = w.child_window(title="Address", control_type="ToolBar")
                    folder_path = address_bar.texts()[0]
                    return folder_path
                except Exception:
                    continue
        return None
    except Exception as e:
        print("❌ Error getting active folder:", e)
        return None



class SmartFileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        # Store a tuple: (event_type, path, timestamp) to track the last event
        self.last_event_info = ("", "", 0)

    def _is_duplicate(self, event_type, path):
        """Checks if the event is a duplicate of the last one."""
        last_type, last_path, last_time = self.last_event_info
        current_time = time.time()
        
        # If the same event on the same path happened less than 0.5s ago, it's a duplicate.
        if event_type == last_type and path == last_path and (current_time - last_time) < 0.5:
            logging.info(f"Debouncing duplicate event: {event_type} on {path}")
            return True
        
        self.last_event_info = (event_type, path, current_time)
        return False

    def on_created(self, event):
        if event.is_directory:
            return
        if self._is_duplicate("created", event.src_path):
            return
        
        time.sleep(2)
        log_file_event("created", event.src_path, source="Active Folder Watcher")

    def on_moved(self, event):
        if event.is_directory:
            return
        # For 'moved', the important path is the destination.
        if self._is_duplicate("moved", event.dest_path):
            return
        
        log_file_event("moved", event.dest_path, source="Active Folder Watcher", extra={"from": event.src_path})

    def on_deleted(self, event):
        if event.is_directory:
            return
        if self._is_duplicate("deleted", event.src_path):
            return

        log_file_event("deleted", event.src_path, source="Active Folder Watcher")

    def on_modified(self, event):
        if event.is_directory:
            return
        if self._is_duplicate("modified", event.src_path):
            return

        log_file_event("modified", event.src_path, source="Active Folder Watcher")

    # def on_any_event(self, event):
    #     if event.is_directory:
    #         return
        
    #     if event.event_type == "created":
    #         time.sleep(2)
        
        
    #     log_file_event(event.event_type, event.src_path,source="Active Folder Watcher")


class ExplorerWatcher:
    def __init__(self):
        self.current_path = None
        self.observer = None
        self.event_handler = SmartFileHandler()
        logging.info("ExplorerWatcher initialized.")

    def get_explorer_path(self):
        try:
            pythoncom.CoInitialize()  # Safe initialization for COM in threads
            shell = win32com.client.Dispatch("Shell.Application")
            windows = shell.Windows()
            for window in windows:
                if window.Name == "File Explorer":
                    folder = window.Document.Folder.Self.Path
                    logging.info(f"Detected folder: {folder}")
                    return folder
        except Exception as e:
            logging.error(f"Error reading explorer window: {e}", exc_info=True)
        return None
    

  

    def watch_active_folder(self):
        logging.info("Starting watch_active_folder loop.")
        try:
            while True:
                new_path = self.get_explorer_path()

                # Handle valid new path
                if new_path and os.path.exists(new_path):
                    if new_path.startswith("::{"):
                        logging.info(f"Ignoring virtual folder: {new_path}")
                    elif new_path != self.current_path:
                        logging.info(f"Switching to watch: {new_path}")

                        if self.observer:
                            self.observer.stop()
                            self.observer.join()

                        self.current_path = new_path
                        self.observer = Observer()
                        self.observer.schedule(self.event_handler, new_path, recursive=False)
                        self.observer.start()
                        logging.info(f"Observer started for: {new_path}")
                    else:
                        # Same folder; do nothing, just wait
                        pass

                else:
                    # Explorer closed or invalid folder
                    if self.current_path is not None:
                        logging.info("No active folder detected. Stopping watcher.")
                        if self.observer:
                            self.observer.stop()
                            self.observer.join()
                            self.observer = None
                        self.current_path = None

                time.sleep(3)

        except KeyboardInterrupt:
            logging.info("Interrupted by user.")

        except Exception as e:
            logging.error(f"Unexpected Error in watch_active_folder: {e}", exc_info=True)

        finally:
            logging.info("Watcher loop finished.")
            if self.observer:
                self.observer.stop()
                self.observer.join()
            

                  
                    
