from N1 import SQLiteDB
from typing import Dict, Any
def create_tables() -> Dict[str, Any]:
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
            # Добавляем пользователей
            users = [
                (1, "Марк", "frizenmarkv@gmail.com"),
                (2, "Влад", "vladislav@gmail.com")
            ]
            for user in users:
                db.execute(
                    "INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)",
                    user
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
                (1, "Ноутбук", 100000, "Электроника", 10),
                (2, "Смартфон", 15000, "Электроника", 25),
                (3, "Книга", 1000, "Литература", 50)
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
                    (1, 2, 3, 5, 5000, "доставлено")
                )
        return {
            "success": True,
            "message": f"Создано таблиц: {len(tables_created)}",
            "tables": tables_created
        }
    finally:
        db.close()
if __name__ == "__main__":
    result = create_tables()
    if result["success"]:
        print(f"Успешно: {result['message']}")
        print(f"Таблицы: {', '.join(result.get('tables', []))}")
    else:
        print(f"Ошибка: {result.get('error', 'Неизвестная ошибка')}")