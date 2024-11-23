from pymongo import MongoClient
from bson.objectid import ObjectId
import sys

# Підключення до бази даних


def get_database():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        return client["cats_db"]
    except Exception as e:
        print(f"Помилка підключення до MongoDB: {e}")
        sys.exit()


# Ініціалізація бази даних і колекції
db = get_database()
collection = db["cats"]

# --------------------- CRUD ОПЕРАЦІЇ ---------------------

# CREATE: Додати нового кота


def add_cat(name, age, features):
    try:
        cat = {"name": name, "age": age, "features": features}
        result = collection.insert_one(cat)
        print(f"Кота додано з _id: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка під час додавання кота: {e}")

# READ: Отримати всіх котів


def get_all_cats():
    try:
        cats = list(collection.find())
        if not cats:
            print("Колекція порожня.")
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка під час отримання всіх котів: {e}")

# READ: Отримати кота за ім'ям


def get_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if not cat:
            print(f"Кота з ім'ям {name} не знайдено.")
        else:
            print(cat)
    except Exception as e:
        print(f"Помилка під час пошуку кота: {e}")

# UPDATE: Оновити вік кота за ім'ям


def update_cat_age(name, new_age):
    try:
        result = collection.update_one(
            {"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Вік кота з ім'ям {name} оновлено.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка під час оновлення віку: {e}")

# UPDATE: Додати характеристику до кота за ім'ям


def add_feature_to_cat(name, feature):
    try:
        result = collection.update_one(
            {"name": name}, {"$push": {"features": feature}})
        if result.matched_count > 0:
            print(f"Характеристику '{feature}' додано коту з ім'ям {name}.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка під час додавання характеристики: {e}")

# DELETE: Видалити кота за ім'ям


def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кота з ім'ям {name} видалено.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка під час видалення кота: {e}")

# DELETE: Видалити всіх котів


def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"Усі записи видалено. Кількість видалених записів: {
              result.deleted_count}")
    except Exception as e:
        print(f"Помилка під час видалення всіх записів: {e}")

# --------------------- ГОЛОВНЕ МЕНЮ ---------------------


def main():
    while True:
        print("\n--- Меню ---")
        print("1. Додати кота")
        print("2. Показати всіх котів")
        print("3. Знайти кота за ім'ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота за ім'ям")
        print("7. Видалити всіх котів")
        print("8. Вийти")

        choice = input("Виберіть опцію: ")

        if choice == "1":
            name = input("Ім'я кота: ")
            age = int(input("Вік кота: "))
            features = input("Характеристики (через кому): ").split(",")
            add_cat(name, age, features)
        elif choice == "2":
            get_all_cats()
        elif choice == "3":
            name = input("Ім'я кота: ")
            get_cat_by_name(name)
        elif choice == "4":
            name = input("Ім'я кота: ")
            new_age = int(input("Новий вік: "))
            update_cat_age(name, new_age)
        elif choice == "5":
            name = input("Ім'я кота: ")
            feature = input("Нова характеристика: ")
            add_feature_to_cat(name, feature)
        elif choice == "6":
            name = input("Ім'я кота: ")
            delete_cat_by_name(name)
        elif choice == "7":
            delete_all_cats()
        elif choice == "8":
            print("До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
