import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('game_scores.db')

# Check if the connection is successful
try:
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a simple query to check if the database is connected
    cursor.execute("SELECT SQLITE_VERSION()")
    data = cursor.fetchone()
    print("SQLite version:", data[0])  # If no errors, print the SQLite version
except sqlite3.Error as e:
    print("SQLite connection error:", e)  # If there's an error, print the error message
finally:
    # Close the database connection
    conn.close()
