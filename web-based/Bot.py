import webview
import os, sys
import subprocess
import threading

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DJANGO_DIR = os.path.join(BASE_DIR, 'auto_writer')

def run_django():
    cur_dir = os.getcwd()
    os.chdir(DJANGO_DIR)

    if sys.platform == "win32":
        # Hide console window on Windows
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(
            ["python", "manage.py", "runserver", "0.0.0.0:8000"],
            startupinfo=startupinfo,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        # For macOS and Linux: redirect output to suppress terminal window
        subprocess.Popen(
            ["python3", "manage.py", "runserver", "0.0.0.0:8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    os.chdir(cur_dir)

# Start Django in background
threading.Thread(target=run_django, daemon=True).start()

webview.create_window("Auto Writer", "http://127.0.0.1:8000/")
webview.start()
