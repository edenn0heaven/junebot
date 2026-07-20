import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "database.db"


# ---------------------------- SAVED POEMS

def save_poem(user_id, poem, poem_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO saved_poems(user_id, poem, poem_id)
        VALUES (?, ?, ?)
    """, (user_id, poem, poem_id))

    conn.commit()
    conn.close()

def get_saved_poems(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT poem_id, poem
        FROM saved_poems
        WHERE user_id = ?
        ORDER BY rowid DESC
    """, (user_id,))

    poems = cursor.fetchall()

    conn.close()

    return poems

def get_last_poem(channel_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message_id
        FROM last_poems
        WHERE channel_id = ?
    """, (channel_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def save_last_poem(channel_id, message_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO last_poems(channel_id, message_id)
        VALUES (?, ?)
        ON CONFLICT(channel_id)
        DO UPDATE SET message_id = excluded.message_id
    """, (channel_id, message_id))

    conn.commit()
    conn.close()

def get_saved_poem(user_id, poem_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT poem
        FROM saved_poems
        WHERE user_id = ? AND poem_id = ?
    """, (user_id, poem_id))

    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

# ---------------------------- DAILY POEM

def get_daily_poem():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT poem FROM daily_poems WHERE date = ?",
        (date.today().isoformat(),)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def save_daily_poem(poem):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO daily_poems(date, poem)
        VALUES (?, ?)
        """,
        (date.today().isoformat(), poem)
    )

    conn.commit()
    conn.close()