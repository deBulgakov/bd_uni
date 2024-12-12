import pg8000.native


# 1. Вывести все данные о курьерах
# 2. Найти всех курьеров, которые используют велосипед как транспорт
# 3. Поиск провайдеров с рейтингом выше среднего и диапазоном цен ниже указанного
# 4. Вывести все заказы, сделанные пользователями с номером телефона заканчивающимся на '31'
# 5. Список блюд с самым высоким содержанием белков
# 6. Посчитать средний рейтинг курьеров
# 7. Список заказов для каждого пользователя с деталями блюда и провайдера
# 8. Курьеры с максимальным и минимальным рейтингом для каждого типа транспорта
# 9. Среднее количество заказов на каждого пользователя в месяц
# 10. Пользователи с максимальной потраченной суммой или максимальным числом заказов
# 11. Пользователи, заказавшие больше всего блюд за последний месяц
# 12. Рейтинг провайдеров по доходам и количество заказов
# 13. Процентная доля заказов каждого курьера за всё время
# 14. Самые популярные блюда по числу заказов, сгруппированные по провайдерам


def bob(x, con):
    match x:
        case 1:
            return con.run('SELECT * FROM yandex_eats_ph.courier')
        case 2:
            return con.run(f"SELECT * FROM yandex_eats_ph.courier WHERE transport = 'Bicycle'")
        case 3:
            return con.run(f'''SELECT 
    name,
    rating,
    price_range
FROM 
    yandex_eats_ph.provider
WHERE 
    rating > (SELECT AVG(rating) FROM yandex_eats_ph.provider)
    AND price_range < 3
ORDER BY 
    rating DESC;
''')
        case 4:
            return con.run(f"SELECT order_id FROM yandex_eats_ph.order WHERE person_id in "
                           f"(SELECT person_id FROM yandex_eats_ph.person WHERE phone_number::text LIKE '%31')")
        case 5:
            return con.run(f'''SELECT 
    d.dish_id,
    d.contains,
    d.nutrients_cfp.proteins AS proteins,
    p.name AS provider_name
FROM 
    yandex_eats_ph.dishes d
JOIN 
    yandex_eats_ph.provider p ON d.provider_id = p.provider_id
ORDER BY 
    proteins DESC
LIMIT 10;
''')
        case 6:
            return con.run(f"SELECT AVG(rating) AS average_courier_rating FROM yandex_eats_ph.courier;")
        case 7:
            return con.run(f'''SELECT 
    p.full_name AS person_name,
    o.order_id,
    d.dish_id,
    d.contains AS dish_contents,
    pr.name AS provider_name,
    o.price
FROM 
    yandex_eats_ph."order" o
JOIN 
    yandex_eats_ph.person p ON o.person_id = p.person_id
JOIN 
    yandex_eats_ph.order_dishes od ON o.order_id = od.order_id
JOIN 
    yandex_eats_ph.dishes d ON od.dish_id = d.dish_id
JOIN 
    yandex_eats_ph.provider pr ON d.provider_id = pr.provider_id;
''')
        case 8:
            return con.run(f'''
    WITH CourierRatings AS (
    SELECT 
        transport,
        name,
        rating,
        ROW_NUMBER() OVER (PARTITION BY transport ORDER BY rating DESC) AS rank_max,
        ROW_NUMBER() OVER (PARTITION BY transport ORDER BY rating ASC) AS rank_min
    FROM 
        yandex_eats_ph.courier
)
    SELECT 
        transport,
        MAX(CASE WHEN rank_max = 1 THEN name END) AS top_courier,
        MAX(CASE WHEN rank_min = 1 THEN name END) AS bottom_courier
    FROM 
        CourierRatings
    GROUP BY 
        transport;
''')
        case 9:
            return con.run(f'''
    SELECT 
    TO_CHAR(datetime_start, 'YYYY-MM') AS month,
    COUNT(order_id) / NULLIF(COUNT(DISTINCT p.person_id), 0) AS avg_orders_per_user
FROM 
    yandex_eats_ph."order" o
JOIN 
    yandex_eats_ph.person p ON o.person_id = p.person_id
GROUP BY 
    TO_CHAR(datetime_start, 'YYYY-MM')
ORDER BY 
    month DESC;
''')
        case 10:
            return con.run(f'''WITH UserStats AS (
    SELECT 
        p.person_id,
        p.full_name,
        COUNT(o.order_id) AS total_orders,
        SUM(o.price) AS total_spent
    FROM 
        yandex_eats_ph.person p
    JOIN 
        yandex_eats_ph."order" o ON p.person_id = o.person_id
    GROUP BY 
        p.person_id, p.full_name
)
SELECT 
    full_name,
    total_orders,
    total_spent
FROM 
    UserStats
WHERE 
    total_spent = (SELECT MAX(total_spent) FROM UserStats)
    OR total_orders = (SELECT MAX(total_orders) FROM UserStats);
''')
        case 11:
            return con.run(f'''WITH LastMonthOrders AS (
    SELECT 
        o.person_id,
        COUNT(od.dish_id) AS dishes_count,
        MAX(o.datetime_start) AS last_order_date
    FROM 
        yandex_eats_ph."order" o
    JOIN 
        yandex_eats_ph.order_dishes od ON o.order_id = od.order_id
    WHERE 
        o.datetime_start >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'
    GROUP BY 
        o.person_id
)
SELECT 
    lm.person_id,
    p.full_name,
    lm.dishes_count,
    lm.last_order_date
FROM 
    LastMonthOrders lm
JOIN 
    yandex_eats_ph.person p ON lm.person_id = p.person_id
WHERE 
    lm.dishes_count = (SELECT MAX(dishes_count) FROM LastMonthOrders);
''')
        case 12:
            return con.run(f'''SELECT 
    p.provider_id,
    p.name AS provider_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.price) AS total_revenue,
    RANK() OVER (ORDER BY SUM(o.price) DESC) AS revenue_rank,
    RANK() OVER (ORDER BY COUNT(o.order_id) DESC) AS orders_rank
FROM 
    yandex_eats_ph.provider p
JOIN 
    yandex_eats_ph."order" o ON p.provider_id = o.provider_id
GROUP BY 
    p.provider_id, p.name
ORDER BY 
    revenue_rank, orders_rank;
''')
        case 13:
            return con.run(f'''SELECT 
    c.courier_id,
    c.name,
    COUNT(o.order_id) AS courier_orders,
    COUNT(o.order_id) * 100.0 / SUM(COUNT(o.order_id)) OVER () AS order_share
FROM 
    yandex_eats_ph.courier c
LEFT JOIN 
    yandex_eats_ph."order" o ON c.courier_id = o.courier_id
GROUP BY 
    c.courier_id, c.name
ORDER BY 
    order_share DESC;   
''')
        case 14:
            return con.run(f'''WITH DishPopularity AS (
    SELECT 
        d.dish_id,
        d.contains AS dish_name,
        d.provider_id,
        COUNT(od.order_id) AS order_count,
        RANK() OVER (PARTITION BY d.provider_id ORDER BY COUNT(od.order_id) DESC) AS rank
    FROM 
        yandex_eats_ph.dishes d
    JOIN 
        yandex_eats_ph.order_dishes od ON d.dish_id = od.dish_id
    GROUP BY 
        d.dish_id, d.contains, d.provider_id
)
SELECT 
    dp.order_count,
    dp.dish_name,
    dp.provider_id,
    p.name AS provider_name
FROM 
    DishPopularity dp
JOIN 
    yandex_eats_ph.provider p ON dp.provider_id = p.provider_id
WHERE 
    dp.rank = 1
ORDER BY 
    dp.order_count DESC;
''')
        case 15:
            return con.run(f"")


connection = pg8000.native.Connection("postgres", password="123123")

x = int(input())
for i in bob(x, connection):
    print(i)

connection.close()


