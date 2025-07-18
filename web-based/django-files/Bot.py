import webview
import os
import sys
import subprocess
import threading
import signal
import time

# Detect if running on Windows
if sys.platform != "win32":
    sys.exit(1)

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DJANGO_DIR = os.path.join(BASE_DIR, 'auto_writer')
django_process = None


def run_django():
    global django_process
    cur_dir = os.getcwd()
    os.chdir(DJANGO_DIR)

    # Run Django with CREATE_NEW_PROCESS_GROUP to allow CTRL_BREAK_EVENT later
    django_process = subprocess.Popen(
        ["python", "manage.py", "runserver", "0.0.0.0:8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

    os.chdir(cur_dir)


# Start Django server in background thread
threading.Thread(target=run_django, daemon=True).start()

# Launch GUI window (blocks until user closes it)
webview.create_window("Auto Writer", "http://127.0.0.1:8000/")
webview.start()

# After GUI closes, stop Django server
if django_process:
    try:
        # Attempt to terminate the Django process
        django_process.terminate()
        # Wait for a short period to allow the process to close
        time.sleep(1)
        if django_process.poll() is None:  # Check if the process is still running
            django_process.kill()  # Force kill if still running
    except Exception as e:
        pass
