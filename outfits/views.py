import sqlite3
from django.shortcuts import render
from db.database import get_connection


def outfit_list(request):
    """Список образов с подсчетом стоимости и проверкой полноты."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    # ДОБАВЛЕНО: o.user_id в SELECT
    outfits = conn.execute("""
        SELECT o.id, o.user_id, o.name, o.season, u.name AS user_name,
               COUNT(oi.clothing_item_id) AS items_count,
               COALESCE(SUM(ci.price), 0) AS total_cost,
               CASE o.occasion
                   WHEN 'casual' THEN 'Повседневный'
                   WHEN 'business' THEN 'Деловой'
                   WHEN 'evening' THEN 'Вечерний'
                   WHEN 'sport' THEN 'Спортивный'
                   WHEN 'festive' THEN 'Праздничный'
                   ELSE o.occasion
               END AS occasion_display
        FROM outfits o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN outfit_items oi ON o.id = oi.outfit_id
        LEFT JOIN clothing_items ci ON oi.clothing_item_id = ci.id
        GROUP BY o.id, o.user_id, o.name, o.season, u.name
        ORDER BY o.name
    """).fetchall()

    outfits_data = []
    for row in outfits:
        outfit = dict(row)

        conn2 = get_connection()
        categories = conn2.execute("""
            SELECT cat.name
            FROM outfit_items oi
            JOIN clothing_items ci ON oi.clothing_item_id = ci.id
            JOIN categories cat ON ci.category_id = cat.id
            WHERE oi.outfit_id = ?
        """, [outfit['id']]).fetchall()
        conn2.close()

        cat_names = {cat['name'] for cat in categories}
        outfit['is_complete'] = 'верх' in cat_names and 'низ' in cat_names
        outfits_data.append(outfit)

    conn.close()
    return render(request, "outfits/outfit_list.html", {"outfits": outfits_data})


def outfit_detail(request, outfit_id):
    """Детальная страница образа."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    # ДОБАВЛЕНО: o.user_id в SELECT
    outfit = conn.execute("""
        SELECT o.id, o.user_id, o.name, o.season, u.name AS user_name,
               CASE o.occasion
                   WHEN 'casual' THEN 'Повседневный'
                   WHEN 'business' THEN 'Деловой'
                   WHEN 'evening' THEN 'Вечерний'
                   WHEN 'sport' THEN 'Спортивный'
                   WHEN 'festive' THEN 'Праздничный'
                   ELSE o.occasion
               END AS occasion_display
        FROM outfits o
        JOIN users u ON o.user_id = u.id
        WHERE o.id = ?
    """, [outfit_id]).fetchone()

    if outfit is None:
        conn.close()
        return render(request, "outfits/404.html", status=404)

    items = conn.execute("""
        SELECT ci.id, ci.name, ci.color, ci.price, cat.name AS category_name
        FROM outfit_items oi
        JOIN clothing_items ci ON oi.clothing_item_id = ci.id
        LEFT JOIN categories cat ON ci.category_id = cat.id
        WHERE oi.outfit_id = ?
    """, [outfit_id]).fetchall()

    total_cost = sum(item['price'] for item in items)
    cat_names = {item['category_name'] for item in items if item['category_name']}
    is_complete = 'верх' in cat_names and 'низ' in cat_names

    conn.close()

    outfit_dict = dict(outfit)
    outfit_dict['total_cost'] = total_cost
    outfit_dict['is_complete'] = is_complete
    outfit_dict['items'] = [dict(item) for item in items]

    return render(request, "outfits/outfit_detail.html", {
        "outfit": outfit_dict,
    })


def statistics(request):
    """Статистика по категориям"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    stats = conn.execute("""
        SELECT cat.name AS category_name,
               COUNT(ci.id) AS items_count,
               COALESCE(SUM(ci.price * ci.quantity), 0) AS total_cost
        FROM categories cat
        LEFT JOIN clothing_items ci ON cat.id = ci.category_id
        GROUP BY cat.id, cat.name
        ORDER BY items_count DESC
    """).fetchall()
    conn.close()
    return render(request, "outfits/statistics.html", {"stats": stats})