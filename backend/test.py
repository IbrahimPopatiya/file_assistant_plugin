import sqlite3

# Path to your database file
conn = sqlite3.connect("file_events.db")
cursor = conn.cursor()

# Example 1: Get all sorted by newest
query = "SELECT * FROM file_events ORDER BY timestamp DESC;"
cursor.execute(query)

# Fetch and print results
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
