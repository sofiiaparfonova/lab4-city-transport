import psycopg

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/city_transport"


def test_connection():
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            result = conn.execute("SELECT current_database()").fetchone()
            print(f"Успішне підключення до бази даних: {result[0]}")
    except psycopg.Error as error:
        print(f"Помилка підключення: {error}")


if __name__ == "__main__":
    test_connection()
