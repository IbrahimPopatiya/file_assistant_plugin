import sys
import subprocess
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.config import DB_PATH


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

HISTORY_UI = os.path.join(FRONTEND_DIR, "history_viewer_ui.py")
AI_UI = os.path.join(FRONTEND_DIR, "ai_assistant_ui.py")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_assistant_launcher.py [history|ai]")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "history":
        subprocess.Popen(["python", HISTORY_UI])
    elif mode == "ai":
        subprocess.Popen(["python", AI_UI])
    else:
        print("Unknown mode:", mode)


