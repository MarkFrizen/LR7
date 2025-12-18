import sqlite3
import time
from typing import Dict, Any, Tuple
class Database:
    """Базовый класс для работы с БД"""
    def connect(self) -> bool:
        raise NotImplementedError
    def execute(self, query: str, params: Tuple = ()) -> Dict[str, Any]:
        raise NotImplementedError
    def close(self) -> None:
        raise NotImplementedError
class SQLiteDB(Database):
    def __init__(self, db_path: str = "lab7.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    def connect(self) -> bool:
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error:
            return False
    def execute(self, query: str, params: Tuple = ()) -> Dict[str, Any]:
        try:
            start_time = time.time()
            self.cursor.execute(query, params)
            result = {"success": True}
            if query.strip().upper().startswith("SELECT"):
                # Для SELECT запросов получаем данные
                columns = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
                result["data"] = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            else:
                # Для остальных запросов коммитим изменения
                self.conn.commit()
                result["rows_affected"] = self.cursor.rowcount
            result["execution_time"] = time.time() - start_time
            return result
        except sqlite3.Error as e:
            return {"success": False, "error": str(e)}
    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
def create_sqlite_db() -> Dict[str, Any]:
    """Создание БД SQLite и таблицы"""
    db = SQLiteDB()
    if not db.connect():
        return {"success": False, "error": "Не удалось подключиться к SQLite"}
    try:
        # Создание таблицы
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        result = db.execute(create_table_query)
        if not result["success"]:
            return result
        # Добавление тестовых данных
        users = [
            (1, "Иван Иванов", "ivan@example.com"),
            (2, "Мария Петрова", "maria@example.com"),
            (3, "Алексей Сидоров", "alex@example.com")
        ]
        inserted = 0
        for user in users:
            insert_result = db.execute(
                "INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)",
                user
            )
            if insert_result["success"]:
                inserted += 1
        # Проверяем, что таблица создана и содержит данные
        check_result = db.execute("SELECT COUNT(*) as count FROM users")
        return {
            "success": True,
            "message": f"БД SQLite и таблица users созданы. Добавлено {inserted} записей.",
            "execution_time": result.get("execution_time", 0),
            "total_records": check_result.get("data", [{"count": 0}])[0]["count"] if check_result["success"] else 0
        }
    finally:
        db.close()
if __name__ == "__main__":
    # Тестируем функцию
    result = create_sqlite_db()
    print("Результат выполнения:")
    print(result)
    # Проверяем, что файл БД создался
    import os
    if os.path.exists("lab7.db"):
        print(f"\nФайл БД создан: {os.path.getsize('lab7.db')} байт")
        # Проверяем содержимое
        conn = sqlite3.connect("lab7.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Таблицы в БД: {[t[0] for t in tables]}")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(f"Записей в таблице users: {len(users)}")
        for user in users:
            print(f"  ID: {user[0]}, Имя: {user[1]}, Email: {user[2]}")
        conn.close()
    else:
        print("Файл БД не создан")