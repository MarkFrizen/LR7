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
            # Выполнение запроса
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
def run():
    """Работа с PostgreSQL через psycopg2"""
    db = PostgreSQLManager()
    connection_result = db.connect()
    print(connection_result.get("message", "Подключено"))
    try:
        # Создание таблицы employees
        create_query = """
            CREATE TABLE IF NOT EXISTS employees3 (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                department VARCHAR(50),
                salary DECIMAL(10, 2),
                hire_date DATE DEFAULT CURRENT_DATE
            )
        """
        db.execute(create_query)
        # Добавление сотрудников
        employees = [
            ("Иван", "Иванов", "ivanov@company.com", "Разработка", 150000),
            ("Мария", "Петрова", "petrova@company.com", "Дизайн", 120000),
            ("Алексей", "Сидоров", "sidorov@company.com", "Разработка", 130000),
            ("Елена", "Кузнецова", "kuznetsova@company.com", "Маркетинг", 110000),
            ("Дмитрий", "Смирнов", "smirnov@company.com", "Разработка", 145000),
            ("Ольга", "Попова", "popova@company.com", "HR", 95000),
            ("Сергей", "Васильев", "vasilyev@company.com", "Дизайн", 115000),
            ("Наталья", "Морозова", "morozova@company.com", "Маркетинг", 105000),
            ("Андрей", "Федоров", "fedorov@company.com", "Разработка", 138000),
            ("Татьяна", "Зайцева", "zaitseva@company.com", "HR", 98000)
        ]
        rows_added = 0
        for emp in employees:
            result = db.execute(
                "INSERT INTO employees3 (first_name, last_name, email, department, salary) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING",
                emp
            )
            if result["success"]:
                rows_added += result.get("rows_affected", 0)
        print(f"Добавлено сотрудников: {rows_added}")
        # Сложный запрос
        complex_query = """
            SELECT 
                e.first_name, 
                e.last_name AS full_name,
                e.department,
                e.salary
            FROM employees3 e
            ORDER BY e.salary DESC
        """
        complex_result = db.execute(complex_query)
        if complex_result["success"]:
            sample_data = complex_result.get("data", [])
            print("Пример данных из таблицы employees3:")
            for row in sample_data:
                print(f"  {row['full_name']}: {row['department']}, {row['salary']}")
        print(complex_result["execution_time"])
    finally:
        db.close()
if __name__ == "__main__":
    run()
