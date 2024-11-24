import psycopg2
from faker import Faker
from dotenv import load_dotenv
import os

# Завантаження змінних з .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cursor = conn.cursor()
faker = Faker()

# Додавання статусів
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute(
        "INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING", (status,))

# Додавання користувачів
for _ in range(10):
    fullname = faker.name()
    email = faker.unique.email()
    cursor.execute(
        "INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

# Додавання завдань
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM status")
status_ids = [row[0] for row in cursor.fetchall()]

for _ in range(50):
    title = faker.sentence(nb_words=4)
    description = faker.text()
    status_id = faker.random.choice(status_ids)
    user_id = faker.random.choice(user_ids)
    cursor.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
        (title, description, status_id, user_id)
    )

# Коміт і закриття підключення
conn.commit()
cursor.close()
conn.close()
