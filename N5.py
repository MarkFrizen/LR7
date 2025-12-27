from typing import Dict, Any
import sqlite3
def print_users(users):
    print(f"{'ID':<4} {'Имя':<20} {'Email':<25}")
    print("-" * 50)
    for user in users:
        print(f"{user[0]:<4} {user[1]:<20} {user[2]:<25}")
def test(a: int = 7):
    print(a)
def delete_record(user_id: int = 7) -> Dict[str, Any]:
    """
    Задание 5: Удалить запись
    """
    # Подключаемся к БД из задания 1
    try:
        conn = sqlite3.connect('lab7.db')
        cursor = conn.cursor()
        # Шаг 3: Показываем текущее состояние (до удаления)
        print("\nТЕКУЩЕЕ СОСТОЯНИЕ ТАБЛИЦЫ 'users':")
        cursor.execute("SELECT * FROM users ORDER BY id")
        current_users = cursor.fetchall()
        print_users(current_users)
        # Удаляем запись
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        rows_deleted = cursor.rowcount
        if rows_deleted > 0:
            conn.commit()
            # Показываем результат
            print(f"\nЗАПИСЬ УДАЛЕНА:")
            print(f"   Удалено записей: {rows_deleted}")
            # Показываем новое состояние
            cursor.execute("SELECT * FROM users ORDER BY id")
            remaining_users = cursor.fetchall()
            print(f"\nНОВОЕ СОСТОЯНИЕ ТАБЛИЦЫ 'users':")
            print_users(remaining_users)
            conn.close()
            return {'success': True}
        else:
            conn.close()
            print(f"\nЗАПИСЬ НЕ УДАЛЕНА")
            return {'success': False, 'error': 'Не удалось удалить запись'}
    except sqlite3.Error as e:
        return {'success': False, 'error': f'Ошибка SQLite: {e}'}
if __name__ == "__main__":
    result = delete_record(3)  # Удаляем запись с ID=2
    print(f"\n Результат задания 5:")
    print(f"   Успешно: {result['success']}")
    if 'error' in result:
        print(f"   Ошибка: {result['error']}")