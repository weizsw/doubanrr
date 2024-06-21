import sqlite3

conn = sqlite3.connect("doubanrr.db")
# Creates the database if it doesn't exist
c = conn.cursor()

# Create table
c.execute(
    """
    CREATE TABLE IF NOT EXISTS tokens_table (
        id INTEGER PRIMARY KEY,
        token TEXT NOT NULL UNIQUE,
        type INTEGER NOT NULL,
        added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS imdb_table (
        id INTEGER PRIMARY KEY,
        imdb_id TEXT NOT NULL UNIQUE,
        added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
)

conn.commit()
conn.close()
