import tkinter as tk
import sys
import os

# Create a robust, absolute path to the backend directory
# This ensures modules can be found regardless of how the script is launched
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

from ai_handler import ask_openai
from utils import fetch_and_clean_events, filter_temp_files, build_context_string

# Use absolute path to ensure it works when launched from context menu
DB_PATH = r"C:\ibrahim\file_assistant_plugin\backend\file_events.db"

def run_ai_assistant():
    root = tk.Tk()
    root.title("AI Assistant")
    root.geometry("400x250")

    tk.Label(root, text="AI Assistant", font=("Arial", 14)).pack(pady=5)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    response = tk.Label(root, text="", wraplength=350)
    response.pack(pady=5)

    def on_ask():
        all_events = fetch_and_clean_events()
        filtered_events = filter_temp_files(all_events)
        context = build_context_string(filtered_events)
        question = entry.get()
        answer = ask_openai(question, context)
        response.config(text=answer)

    tk.Button(root, text="Ask", command=on_ask).pack()
    root.mainloop()

if __name__ == "__main__":
    run_ai_assistant()
