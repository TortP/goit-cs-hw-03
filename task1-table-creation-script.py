import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Завантаження змінних з .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# SQL-запити для створення таблиць
CREATE_USERS_TABLE = """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
"""

CREATE_STATUS_TABLE = """
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
"""

CREATE_TASKS_TABLE = """
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

# Функція перевірки існування таблиці


def table_exists(cursor, table_name):
    query = sql.SQL("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = %s
        );
    """)
    cursor.execute(query, (table_name,))
    return cursor.fetchone()[0]

# Функція створення таблиці


def create_table(cursor, table_name, create_query):
    if table_exists(cursor, table_name):
        print(f"Таблиця '{table_name}' вже існує.")
    else:
        cursor.execute(create_query)
        print(f"Таблицю '{table_name}' створено.")

# Основна функція


def create_tables():
    try:
        # Підключення до бази даних PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Створення таблиць із перевіркою
        create_table(cursor, "users", CREATE_USERS_TABLE)
        create_table(cursor, "status", CREATE_STATUS_TABLE)
        create_table(cursor, "tasks", CREATE_TASKS_TABLE)

        # Застосування змін
        conn.commit()

    except psycopg2.Error as e:
        print(f"Помилка під час створення таблиць: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    create_tables()
