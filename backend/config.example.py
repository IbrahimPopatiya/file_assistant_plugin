import os

# Directory to watch — you can change this to your actual path
WATCHED_DIR = os.path.join(os.path.dirname(__file__), "watched")

# Set your OpenAI API key as an environment variable, e.g.:
#   setx OPENAI_API_KEY "sk-..."
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Path to DB file inside backend folder
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "file_events.db")
DB_FILE = DB_PATH
