import sqlite3
from django.shortcuts import render
from db.database import get_connection


def user_list(request):
    """Список пользователей из SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    users = conn.execute(
        """
        SELECT u.id, u.name, u.email,
        COUNT(ci.id) AS items_count,
        COALESCE(SUM(ci.price * ci.quantity), 0) AS total_cost
        FROM users u
        LEFT JOIN clothing_items ci ON u.id = ci.user_id
        GROUP BY u.id, u.name, u.email
        ORDER BY u.name
        """
    ).fetchall()
    conn.close()
    return render(request, "accounts/user_list.html", {"users": users})


def user_detail(request, user_id):
    """Профиль пользователя."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    # Получаем данные пользователя
    user = conn.execute(
        """
        SELECT u.*,
        COUNT(ci.id) AS items_count,
        COALESCE(SUM(ci.price * ci.quantity), 0) AS total_cost
        FROM users u
        LEFT JOIN clothing_items ci ON u.id = ci.user_id
        WHERE u.id = ?
        GROUP BY u.id
        """,
        [user_id],
    ).fetchone()

    if user is None:
        conn.close()
        return render(request, "accounts/404.html", status=404)

    # Получаем список вещей пользователя с переводом сезона и стиля
    clothing_items = conn.execute(
        """
        SELECT ci.id, ci.name, ci.color, ci.price, ci.quantity,
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
        WHERE ci.user_id = ?
        ORDER BY ci.name
        """,
        [user_id],
    ).fetchall()

    conn.close()

    return render(
        request,
        "accounts/user_detail.html",
        {
            "user": user,
            "clothing_items": clothing_items,
        }
    )