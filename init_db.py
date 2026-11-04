from datetime import date

import psycopg

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/city_transport"

routes = [
    (
        "Автобус",
        "3А",
        date(2022, 3, 15),
        "Площа Різні",
        "вул. Стрийська",
        35,
        "Щоденний маршрут",
    ),
    (
        "Трамвай",
        "1",
        date(2021, 5, 10),
        "Залізничний вокзал",
        "Площа Соборна",
        25,
        "Центральний маршрут",
    ),
    (
        "Трамвай",
        "8",
        date(2023, 2, 1),
        "Площа Соборна",
        "вул. Вернадського",
        30,
        "Зручний для студентів",
    ),
    (
        "Тролейбус",
        "22",
        date(2022, 9, 12),
        "Університет",
        "Автовокзал",
        40,
        "Міський маршрут",
    ),
    (
        "Автобус",
        "10",
        date(2020, 6, 20),
        "вул. Зелена",
        "вул. Наукова",
        45,
        "Довгий маршрут",
    ),
    (
        "Трамвай",
        "2",
        date(2021, 4, 5),
        "Пасічна",
        "Залізничний вокзал",
        35,
        "Щоденний маршрут",
    ),
    (
        "Автобус",
        "47А",
        date(2023, 7, 1),
        "вул. Любінська",
        "Площа Різні",
        50,
        "З'єднує райони міста",
    ),
    (
        "Тролейбус",
        "25",
        date(2022, 1, 18),
        "вул. Шота Руставелі",
        "вул. Кульпарківська",
        30,
        "Міський маршрут",
    ),
    ("Автобус", "18", date(2020, 8, 14), "Сихів", "Центр", 40, "Популярний маршрут"),
    (
        "Трамвай",
        "6",
        date(2021, 11, 9),
        "Залізничний вокзал",
        "вул. Миколайчука",
        35,
        "Щоденний маршрут",
    ),
]

stops = [
    ("Залізничний вокзал", "пл. Двірцева"),
    ("Площа Різні", "пл. Різні"),
    ("Площа Соборна", "пл. Соборна"),
    ("Університет", "вул. Університетська"),
    ("Автовокзал", "вул. Стрийська"),
    ("Пасічна", "вул. Пасічна"),
    ("вул. Стрийська", "вул. Стрийська"),
    ("вул. Наукова", "вул. Наукова"),
    ("вул. Зелена", "вул. Зелена"),
    ("вул. Любінська", "вул. Любінська"),
    ("вул. Шота Руставелі", "вул. Шота Руставелі"),
    ("вул. Кульпарківська", "вул. Кульпарківська"),
    ("Сихів", "просп. Червоної Калини"),
    ("Центр", "просп. Свободи"),
    ("вул. Миколайчука", "вул. Миколайчука"),
]

route_stops = [
    (1, 2, 1),
    (1, 7, 2),
    (1, 8, 3),
    (2, 1, 1),
    (2, 3, 2),
    (2, 14, 3),
    (3, 3, 1),
    (3, 13, 2),
    (3, 8, 3),
    (4, 4, 1),
    (4, 5, 2),
    (4, 12, 3),
    (5, 9, 1),
    (5, 8, 2),
    (5, 13, 3),
    (6, 6, 1),
    (6, 3, 2),
    (6, 1, 3),
    (7, 10, 1),
    (7, 2, 2),
    (7, 14, 3),
    (8, 11, 1),
    (8, 12, 2),
    (8, 5, 3),
    (9, 13, 1),
    (9, 14, 2),
    (9, 3, 3),
    (10, 1, 1),
    (10, 15, 2),
    (10, 2, 3),
]


def initialize_database():
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transport_routes (
                id SERIAL PRIMARY KEY,
                transport_type VARCHAR(30) NOT NULL,
                route_number VARCHAR(10) NOT NULL,
                introduction_date DATE NOT NULL DEFAULT CURRENT_DATE,
                start_stop VARCHAR(100) NOT NULL,
                end_stop VARCHAR(100) NOT NULL,
                travel_time INTEGER NOT NULL,
                note TEXT
            )
        """)

        conn.execute("""
            ALTER TABLE transport_routes
            ADD COLUMN IF NOT EXISTS introduction_date DATE
            DEFAULT CURRENT_DATE
        """)

        conn.execute("""
            ALTER TABLE transport_routes
            ADD COLUMN IF NOT EXISTS note TEXT
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS stops (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address VARCHAR(150) NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS route_stops (
                id SERIAL PRIMARY KEY,
                route_id INTEGER REFERENCES transport_routes(id)
                    ON DELETE CASCADE,
                stop_id INTEGER REFERENCES stops(id),
                stop_order INTEGER NOT NULL
            )
        """)

        conn.execute("""
            TRUNCATE TABLE route_stops, stops, transport_routes
            RESTART IDENTITY CASCADE
        """)

        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO transport_routes
                (transport_type, route_number, introduction_date,
                 start_stop, end_stop, travel_time, note)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                routes,
            )

            cur.executemany(
                """
                INSERT INTO stops (name, address)
                VALUES (%s, %s)
            """,
                stops,
            )

            cur.executemany(
                """
                INSERT INTO route_stops (route_id, stop_id, stop_order)
                VALUES (%s, %s, %s)
            """,
                route_stops,
            )

        print("Базу даних успішно створено!")
        print("Маршрути:", len(routes))
        print("Зупинки:", len(stops))
        print("Зв'язки:", len(route_stops))
        print("Усього записів:", len(routes) + len(stops) + len(route_stops))


if __name__ == "__main__":
    initialize_database()
