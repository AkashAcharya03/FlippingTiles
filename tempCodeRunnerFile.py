conn = sqlite3.connect('game_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store player information if it doesn't exist
cursor.execute