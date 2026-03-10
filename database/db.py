import sqlite3
from pathlib import Path

DB_PATH = Path("data/knowledge.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("database/schema.sql", "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()


def insert_item(content: str, source: str = "telegram"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO items (source, content) VALUES (?, ?)",
        (source, content),
    )

    conn.commit()
    conn.close()
