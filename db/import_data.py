import json
from pathlib import Path
from db.database import get_connection

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(filename):
    """Загрузить данные из JSON-файла."""
    filepath = DATA_DIR / filename
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def import_categories(conn):
    """Импорт категорий."""
    categories = load_json("categories.json")
    conn.executemany(
        """INSERT OR IGNORE INTO categories (id, name) VALUES (?, ?)""",
        [(c["id"], c["name"]) for c in categories],
    )


def import_users(conn):
    """Импорт пользователей."""
    users = load_json("users.json")
    conn.executemany(
        """INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)""",
        [(u["id"], u["name"], u["email"]) for u in users],
    )


def import_clothing(conn):
    """Импорт вещей."""
    items = load_json("clothing_items.json")
    conn.executemany(
        """INSERT OR IGNORE INTO clothing_items
           (id, user_id, category_id, name, color, season, style, price, quantity)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            (
                i["id"], i["user_id"], i["category_id"],
                i["name"], i["color"], i["season"], i["style"],
                i["price"], i["quantity"],
            )
            for i in items
        ],
    )


def import_outfits(conn):
    """Импорт образов."""
    outfits = load_json("outfits.json")
    conn.executemany(
        """INSERT OR IGNORE INTO outfits
           (id, user_id, name, occasion, season)
           VALUES (?, ?, ?, ?, ?)""",
        [
            (o["id"], o["user_id"], o["name"], o["occasion"], o["season"])
            for o in outfits
        ],
    )


def import_outfit_items(conn):
    """Импорт связей образ-вещь."""
    items = load_json("outfit_items.json")
    conn.executemany(
        """INSERT OR IGNORE INTO outfit_items
           (outfit_id, clothing_item_id) VALUES (?, ?)""",
        [(i["outfit_id"], i["clothing_item_id"]) for i in items],
    )


def main():
    """Главная функция импорта."""
    conn = get_connection()
    try:
        # ВАЖНО: порядок импорта определяется внешними ключами
        import_categories(conn)   # сначала справочники
        import_users(conn)        # пользователи
        import_clothing(conn)     # вещи (ссылаются на users и categories)
        import_outfits(conn)      # образы (ссылаются на users)
        import_outfit_items(conn) # связи (ссылаются на outfits и clothing_items)
        conn.commit()
        print("Данные успешно импортированы из JSON.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()