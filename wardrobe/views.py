import sqlite3
from django.shortcuts import render
from db.database import get_connection


def clothing_list(request):
    """Список всех вещей из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    items = conn.execute(
        """
        SELECT ci.id, ci.name, ci.color,
               ci.price, ci.quantity,
               cat.name AS category_name, u.name AS user_name,
               CASE ci.season
                   WHEN 'summer' THEN 'Лето'
                   WHEN 'winter' THEN 'Зима'
                   WHEN 'demiseason' THEN 'Демисезон'
                   WHEN 'all_season' THEN 'Всесезон'
                   ELSE ci.season
               END AS season_display,
               CASE ci.style
                   WHEN 'casual' THEN 'Повседневный'
                   WHEN 'formal' THEN 'Деловой'
                   WHEN 'sport' THEN 'Спортивный'
                   WHEN 'street' THEN 'Уличный'
                   WHEN 'classic' THEN 'Классический'
                   WHEN 'romantic' THEN 'Романтический'
                   ELSE ci.style
               END AS style_display
        FROM clothing_items ci
        LEFT JOIN categories cat ON ci.category_id = cat.id
        JOIN users u ON ci.user_id = u.id
        ORDER BY ci.name
        """
    ).fetchall()
    conn.close()
    return render(request, "wardrobe/clothing_list.html", {"items": items})


def clothing_detail(request, item_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    item = conn.execute(
        """
        SELECT ci.*, cat.name AS category_name, 
               u.id AS user_id, u.name AS user_name,
               CASE ci.season
                   WHEN 'summer' THEN 'Лето'
                   WHEN 'winter' THEN 'Зима'
                   WHEN 'demiseason' THEN 'Демисезон'
                   WHEN 'all_season' THEN 'Всесезон'
                   ELSE ci.season
               END AS season_display,
               CASE ci.style
                   WHEN 'casual' THEN 'Повседневный'
                   WHEN 'formal' THEN 'Деловой'
                   WHEN 'sport' THEN 'Спортивный'
                   WHEN 'street' THEN 'Уличный'
                   WHEN 'classic' THEN 'Классический'
                   WHEN 'romantic' THEN 'Романтический'
                   ELSE ci.style
               END AS style_display
        FROM clothing_items ci
        LEFT JOIN categories cat ON ci.category_id = cat.id
        JOIN users u ON ci.user_id = u.id
        WHERE ci.id = ?
        """,
        [item_id],
    ).fetchone()
    conn.close()

    if item is None:
        return render(request, "wardrobe/404.html", status=404)

    return render(request, "wardrobe/clothing_detail.html", {"item": item})


def available_items(request):
    """Поиск вещей по сезону и стилю."""
    season = request.GET.get("season")
    style = request.GET.get("style")
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    query = """
        SELECT ci.name, ci.color, ci.price, 
               cat.name AS category_name,
               CASE ci.season
                   WHEN 'summer' THEN 'Лето'
                   WHEN 'winter' THEN 'Зима'
                   WHEN 'demiseason' THEN 'Демисезон'
                   WHEN 'all_season' THEN 'Всесезон'
                   ELSE ci.season
               END AS season_display,
               CASE ci.style
                   WHEN 'casual' THEN 'Повседневный'
                   WHEN 'formal' THEN 'Деловой'
                   WHEN 'sport' THEN 'Спортивный'
                   WHEN 'street' THEN 'Уличный'
                   WHEN 'classic' THEN 'Классический'
                   WHEN 'romantic' THEN 'Романтический'
                   ELSE ci.style
               END AS style_display
        FROM clothing_items ci
        LEFT JOIN categories cat ON ci.category_id = cat.id
        WHERE 1=1
    """

    params = []
    if season:
        query += " AND ci.season = ?"
        params.append(season)
    if style:
        query += " AND ci.style = ?"
        params.append(style)

    query += " ORDER BY ci.price"

    items = conn.execute(query, params).fetchall()
    conn.close()

    return render(request, "wardrobe/available.html", {
        "items": items,
        "season": season,
        "style": style,
    })