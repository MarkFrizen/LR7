from N1 import SQLiteDB  # Изменено с N1 на task1
from typing import Dict, Any
import sqlite3
def create_multiple_tables() -> Dict[str, Any]:
    """Создание нескольких связанных таблиц"""
    db = SQLiteDB()
    if not db.connect():
        return {"success": False, "error": "Не удалось подключиться к SQLite"}
    try:
        tables_created = []
        # Шаг 1: Проверяем и создаем таблицу users, если её нет
        users_check_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        users_result = db.execute(users_check_query)
        if users_result["success"]:
            tables_created.append("users")
            # Добавляем тестового пользователя, если таблица пуста
            check_empty = db.execute("SELECT COUNT(*) as count FROM users")
            if check_empty["success"] and check_empty.get("data", [{}])[0].get("count", 0) == 0:
                db.execute(
                    "INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)",
                    (1, "Тестовый Пользователь", "test@example.com")
                )
        # Шаг 2: Таблица products
        products_query = """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT,
                stock INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        result1 = db.execute(products_query)
        if result1["success"]:
            tables_created.append("products")
            # Добавляем тестовые товары
            products = [
                (1, "Ноутбук", 99999, "Электроника", 10),
                (2, "Смартфон", 59999, "Электроника", 25),
                (3, "Книга", 1499, "Литература", 50)
            ]
            for product in products:
                db.execute(
                    "INSERT OR IGNORE INTO products (id, name, price, category, stock) VALUES (?, ?, ?, ?, ?)",
                    product
                )
        # Шаг 3: Таблица orders
        orders_query = """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                total_price REAL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """
        result2 = db.execute(orders_query)
        if result2["success"]:
            tables_created.append("orders")
            # Добавляем тестовый заказ, если таблица пуста
            check_orders = db.execute("SELECT COUNT(*) as count FROM orders")
            if check_orders["success"] and check_orders.get("data", [{}])[0].get("count", 0) == 0:
                db.execute(
                    """INSERT OR IGNORE INTO orders 
                       (id, user_id, product_id, quantity, total_price, status) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (1, 1, 1, 1, 99999, "completed")
                )
        # Проверяем созданные таблицы
        check_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        check_result = db.execute(check_query)
        return {
            "success": True,
            "message": f"Создано таблиц: {len(tables_created)}",
            "tables": tables_created,
            "all_tables": [table["name"] for table in check_result.get("data", [])] if check_result["success"] else [],
            "products_count": 3,
            "test_order_created": True
        }
    finally:
        db.close()
# Альтернативная версия с простым SQLite
def create_multiple_tables_simple() -> Dict[str, Any]:
    """Простая версия создания нескольких таблиц"""
    try:
        conn = sqlite3.connect('lab7.db')
        cursor = conn.cursor()
        # Создаем таблицу users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        # Создаем таблицу products
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT
            )
        """)
        # Создаем таблицу orders с внешними ключами
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        # Добавляем тестовые данные
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Иван', 'ivan@example.com')")
        cursor.execute("INSERT OR IGNORE INTO products (id, name, price, category) VALUES (1, 'Ноутбук', 99999, 'Электроника')")
        cursor.execute("INSERT OR IGNORE INTO orders (id, user_id, product_id, quantity) VALUES (1, 1, 1, 1)")
        conn.commit()
        # Проверяем созданные таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return {
            "success": True,
            "message": "Несколько таблиц созданы успешно",
            "tables_created": tables,
            "test_data_added": True
        }
    except sqlite3.Error as e:
        return {"success": False, "error": str(e)}
def verify_table_creation():
    """Проверка создания таблиц"""
    try:
        conn = sqlite3.connect('lab7.db')
        cursor = conn.cursor()
        # Проверяем существование всех таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        print("Таблицы в базе данных:")
        for table in tables:
            print(f"  - {table[0]}")
            # Показываем структуру таблицы
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print(f"    Столбцы: {', '.join([col[1] for col in columns])}")
        conn.close()
        return tables
    except sqlite3.Error as e:
        print(f"Ошибка при проверке таблиц: {e}")
        return []
if __name__ == "__main__":
    print("Задание 7: Создать несколько таблиц")
    print("=" * 50)
    # Вариант 1: Используя SQLiteDB из task1
    print("Вариант 1: Используя класс SQLiteDB")
    result = create_multiple_tables()
    if result["success"]:
        print(f"Успешно: {result['message']}")
        print(f"Таблицы: {', '.join(result.get('tables', []))}")
        print(f"Все таблицы в БД: {', '.join(result.get('all_tables', []))}")
    else:
        print(f"Ошибка: {result.get('error', 'Неизвестная ошибка')}")
    print("\n" + "=" * 50)
    # Вариант 2: Простая версия
    print("Вариант 2: Простая версия")
    result_simple = create_multiple_tables_simple()
    if result_simple["success"]:
        print(f"Успешно: {result_simple['message']}")
        print(f"Созданные таблицы: {', '.join(result_simple.get('tables_created', []))}")
    else:
        print(f"Ошибка: {result_simple.get('error', 'Неизвестная ошибка')}")
    print("\n" + "=" * 50)
    # Проверяем результат
    print("Проверка создания таблиц:")
    verify_table_creation()