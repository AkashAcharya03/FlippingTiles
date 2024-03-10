import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('game_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query to fetch all rows from the scores table
cursor.execute("SELECT * FROM Scores")

# Fetch all rows returned by the SELECT query
rows = cursor.fetchall()

# Print the fetched rows
for row in rows:
    print(row)

# Close the database connection
conn.close()
