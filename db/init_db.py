import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent

conn = sqlite3.connect(BASE_DIR / "database.db")

with open(BASE_DIR / "db.sql", "r", encoding="utf-8") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database created.")