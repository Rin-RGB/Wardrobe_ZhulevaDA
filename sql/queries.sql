-- 1. Список всех вещей
SELECT id, name, color, season, style, price, quantity
FROM clothing_items
ORDER BY name;

-- 2. Список всех пользователей
SELECT id, name, email
FROM users
ORDER BY name;

-- 3. Поиск вещей по сезону (WHERE)
SELECT id, name, color, season
FROM clothing_items
WHERE season = 'summer';

-- 4. Поиск вещей по стилю (WHERE)
SELECT id, name, style, price
FROM clothing_items
WHERE style = 'formal';

-- 5. Вещи конкретного пользователя (WHERE + JOIN)
SELECT ci.name, ci.color, ci.price, u.name AS user_name
FROM clothing_items ci
JOIN users u ON ci.user_id = u.id
WHERE u.id = 1;

-- 6. Полная информация о вещи с категорией и пользователем (JOIN)
SELECT ci.name AS item_name, ci.color, ci.price,
       cat.name AS category_name, u.name AS user_name
FROM clothing_items ci
JOIN categories cat ON ci.category_id = cat.id
JOIN users u ON ci.user_id = u.id
WHERE ci.id = 1;

-- 7. Образы с вещами (JOIN)
SELECT o.name AS outfit_name, o.occasion, ci.name AS item_name
FROM outfits o
JOIN outfit_items oi ON o.id = oi.outfit_id
JOIN clothing_items ci ON oi.clothing_item_id = ci.id
ORDER BY o.name;

-- 8. Количество вещей по категориям (GROUP BY + COUNT)
SELECT cat.name AS category_name, COUNT(ci.id) AS items_count
FROM categories cat
LEFT JOIN clothing_items ci ON cat.id = ci.category_id
GROUP BY cat.id, cat.name
ORDER BY items_count DESC;

-- 9. Общая стоимость гардероба пользователя (SUM)
SELECT u.name AS user_name, SUM(ci.price * ci.quantity) AS total_cost
FROM users u
JOIN clothing_items ci ON u.id = ci.user_id
GROUP BY u.id, u.name
ORDER BY total_cost DESC;

-- 10. Категории с количеством вещей больше 1 (HAVING)
SELECT cat.name AS category_name, COUNT(ci.id) AS items_count
FROM categories cat
JOIN clothing_items ci ON cat.id = ci.category_id
GROUP BY cat.id, cat.name
HAVING COUNT(ci.id) > 1;

-- 11. Поиск вещей по сезону и стилю (параметризованный запрос)
SELECT ci.name, ci.color, ci.price, cat.name AS category_name
FROM clothing_items ci
JOIN categories cat ON ci.category_id = cat.id
WHERE ci.season = ? AND ci.style = ?
ORDER BY ci.price;

-- 12. Статистика по пользователям (GROUP BY)
SELECT u.name AS user_name,
       COUNT(ci.id) AS items_count,
       SUM(ci.price * ci.quantity) AS total_cost
FROM users u
LEFT JOIN clothing_items ci ON u.id = ci.user_id
GROUP BY u.id, u.name
ORDER BY total_cost DESC;