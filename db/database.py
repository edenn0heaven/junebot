import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "database.db"


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