import sqlite3
from datetime import datetime, timedelta
import json
from openai import OpenAI
from config import DB_FILE, OPENAI_API_KEY

# Add debug logging
def debug_log(message):
    print(f"[DEBUG] {message}")

client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_file_events():
    try:
        debug_log("Connecting to database...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Fixed column name from filename to file_name
        cursor.execute("SELECT event_type, file_name, timestamp, file_path FROM file_events")
        rows = cursor.fetchall()
        debug_log(f"Fetched {len(rows)} events from database")
        
        conn.close()

        if not rows:
            debug_log("No events found in database")
            return "No file events found in the database."

        context = ""
        for i, row in enumerate(rows, 1):
            event_type, file_name, event_time, file_path = row
            context += f"{i}. event: {event_type}, file: {file_name}, date: {event_time}, path: {file_path}\n"
        
        debug_log(f"Generated context with {len(rows)} events")
        return context
    except Exception as e:
        debug_log(f"Error in fetch_file_events: {str(e)}")
        return f"Error fetching file events: {str(e)}"

def ask_openai(question, context=""):
    """
    Sends a simple query to OpenAI and returns the answer.
    
    Parameters:
    - question (str): The user's query
    - context (str): Optional context (like file data or summaries)

    Returns:
    - str: Answer from OpenAI
    """
    try:
        debug_log("Preparing to call OpenAI API...")
        debug_log(f"Question: {question}")
        debug_log(f"Context length: {len(context)} characters")

        if not context:
            return "No file events available to answer your question."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You answer clearly based on file history. Format output as a list with filename, directory, event type, and date"},
                {"role": "user", "content": f"{context}\n\nQuestion: {question}\nPlease list each with:\n- File_name\n- Directory\n- Event Type\n- Time" } 
            ],
            temperature=0.5,
            max_tokens=300
        )
        
        debug_log("Successfully received response from OpenAI")
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        debug_log(f"Error in ask_openai: {str(e)}")
        return f"Error: {str(e)}"

# Test function
def test_ai_handler():
    debug_log("Starting AI handler test...")
    
    # Test database connection
    events = fetch_file_events()
    debug_log("Database test completed")
    
    # Test OpenAI connection
    test_question = "What files were deleted last week?"
    debug_log("Testing OpenAI connection...")
    response = ask_openai(test_question, events)
    debug_log("OpenAI test completed")
    
    return response

if __name__ == "__main__":
    print("\n=== Testing AI Handler ===")
    result = test_ai_handler()
    print("\n=== Test Result ===")
    print(result)
    print("===================")



