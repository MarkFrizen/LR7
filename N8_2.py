from typing import Dict, Any, Tuple
import time
import psycopg2
from psycopg2.extras import RealDictCursor
class PostgreSQLManager:
    """Менеджер для работы с PostgreSQL"""
    def __init__(self):
        self.config = {
            "host": "localhost", "port": "5432", "dbname": "lab7_db",
            "user": "postgres", "password": "dSgfe34sa"
        }
        self.conn = None
        self.cursor = None
    def connect(self) -> Dict[str, Any]:
        """Подключение к PostgreSQL с подробными ошибками"""
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            # Проверяем подключение
            self.cursor.execute("SELECT version()")
            version_info = self.cursor.fetchone()
            return {
                "success": True,
                "message": f"Подключено к PostgreSQL {version_info['version']}",
                "database": self.config["dbname"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    def execute(self, query: str, params: Tuple = ()) -> Dict[str, Any]:
        """Выполнение SQL запроса"""
        try:
            if not self.cursor:
                return {"success": False, "error": "Нет активного подключения"}
            start_time = time.time()
            self.cursor.execute(query, params)
            result = {"success": True}
            if query.strip().upper().startswith("SELECT"):
                result["data"] = self.cursor.fetchall()
            else:
                self.conn.commit()
                result["rows_affected"] = self.cursor.rowcount
            result["execution_time"] = time.time() - start_time
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    def close(self) -> None:
        """Закрытие соединения"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

def work_with_postgresql():
    """Работа с PostgreSQL через psycopg2"""
    print("Проверка подключения к PostgreSQL...")
    db = PostgreSQLManager()
    connection_result = db.connect()
    if not connection_result.get("success"):
        return connection_result
    print(connection_result.get("message", "Подключено"))
    try:
        # Создаем предварительную загрузку данных таблицы employees в кэш
        query = """
            -- Установка расширения предварительной загрузки, если не установлено
            CREATE EXTENSION IF NOT EXISTS pg_prewarm;

            -- Загрузка всей таблицы в кеш
            SELECT pg_prewarm('employees');
        """
        result = db.execute(query)
        print(result)
        # Запрос на выборку
        complex_query = """
            SELECT 
                e.first_name || ' ' || e.last_name AS full_name,
                e.department,
                e.salary,
                COUNT(*) OVER (PARTITION BY e.department) as dept_count,
                AVG(e.salary) OVER (PARTITION BY e.department) as avg_dept_salary
            FROM employees e
            ORDER BY e.salary DESC
        """
        complex_result = db.execute(complex_query)

        if complex_result["success"]:
            sample_data = complex_result.get("data", [])[:3]
            print("Пример данных из таблицы employees:")
            for row in sample_data:
                print(f"  {row['full_name']}: {row['department']}, {row['salary']}")
        print(complex_result["execution_time"])

    finally:
        db.close()


if __name__ == "__main__":
    result = work_with_postgresql()
