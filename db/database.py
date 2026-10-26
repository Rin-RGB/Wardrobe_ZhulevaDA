import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "wardrobe.sqlite"


def get_connection():
    """Создать подключение к базе данных."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn
