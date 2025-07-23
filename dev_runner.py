"""
Development runner for Break Reminder with auto-reload (like nodemon).
Requires: pip install watchdog
"""

import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_PATHS = ["src", "break_reminder_enhanced.py"]

class RestartHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback

    def on_any_event(self, event):
        if event.is_directory:
            return
        self.restart_callback()

def run_script():
    return subprocess.Popen([sys.executable, "break_reminder_enhanced.py"])

def main():
    process = run_script()
    restart_pending = [False]

    def restart():
        if not restart_pending[0]:
            restart_pending[0] = True
            process.terminate()
            time.sleep(0.5)
            print("Restarting due to file change...")
            nonlocal process
            process = run_script()
            restart_pending[0] = False

    event_handler = RestartHandler(restart)
    observer = Observer()
    for path in WATCH_PATHS:
        observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            if process.poll() is not None:
                print("Process exited. Restarting...")
                process = run_script()
    except KeyboardInterrupt:
        observer.stop()
        process.terminate()
    observer.join()

if __name__ == "__main__":
    main()
