import sqlite3

from loguru import logger


def set_token(token, token_type):
    conn = sqlite3.connect("./db/doubanrr.db")
    c = conn.cursor()

    c.execute(
        """
        INSERT OR IGNORE INTO tokens_table (token, type)
        VALUES (?, ?)
    """,
        (token, token_type),
    )

    conn.commit()
    conn.close()
    logger.info(f"Token {token}, Token Type {token_type} has been set.")


def update_token(id, new_token, token_type):
    conn = sqlite3.connect("./db/doubanrr.db")
    c = conn.cursor()

    c.execute(
        """
        UPDATE tokens_table
        SET token = ?,
            type = ?,
            added_time = CURRENT_TIMESTAMP
        WHERE id = ?
    """,
        (new_token, token_type, id),
    )

    conn.commit()
    conn.close()
    logger.info(f"Token {new_token}, Token Type {token_type} has been updated.")


def get_token(token_type):
    conn = sqlite3.connect("./db/doubanrr.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT token, added_time
        FROM tokens_table
        WHERE type = ?
        ORDER BY added_time DESC
        LIMIT 1
    """,
        (token_type,),
    )

    result = c.fetchone()

    conn.close()

    return (result[0], result[1]) if result else (None, None)


def set_imdb_record(imdb_id, watched=False):
    conn = sqlite3.connect("./db/doubanrr.db")
    c = conn.cursor()

    c.execute(
        """
        INSERT OR REPLACE INTO imdb_table (imdb_id, watched)
        VALUES (?, ?)
        """,
        (imdb_id, watched),
    )

    conn.commit()
    conn.close()
    logger.info(f"IMDb ID {imdb_id} has been set or updated.")


def get_imdb_record(imdb_id):
    conn = sqlite3.connect("./db/doubanrr.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT imdb_id, watched
        FROM imdb_table
        WHERE imdb_id = ?
    """,
        (imdb_id,),
    )

    result = c.fetchone()

    conn.close()

    return result if result else None
