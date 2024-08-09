import sqlite3

conn = sqlite3.connect("./db/doubanrr.db")
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
        watched BOOLEAN DEFAULT 0,
        added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
)

conn.commit()
conn.close()
