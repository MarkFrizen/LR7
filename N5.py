from typing import Dict, Any
import os
import sqlite3
def ensure_task1_completed() -> Dict[str, Any]:
    """Проверка, что задание 1 выполнено"""
    if not os.path.exists('lab7.db'):
        return {
            'success': False,
            'error': 'Файл lab7.db не найден. Сначала выполните задание 1.',
            'action_required': 'Выполнить create_sqlite_db() из задания 1'
        }
    try:
        conn = sqlite3.connect('lab7.db')
        cursor = conn.cursor()
        # Проверяем таблицу users (из задания 1)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone()
        if not table_exists:
            conn.close()
            return {
                'success': False,
                'error': 'Таблица users не существует. Сначала выполните задание 1.',
                'action_required': 'Выполнить create_sqlite_db() из задания 1'
            }
        # Проверяем, есть ли данные в таблице
        cursor.execute("SELECT COUNT(*) as count FROM users")
        count_result = cursor.fetchone()
        conn.close()
        if count_result[0] == 0:
            return {
                'success': False,
                'error': 'Таблица users пуста. Сначала выполните задание 1.',
                'action_required': 'Выполнить create_sqlite_db() из задания 1'
            }
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': f'Ошибка при проверке БД: {e}'}
def delete_record(user_id: int = 2) -> Dict[str, Any]:
    """
    Задание 5: Удалить запись
    Явно связан с заданием 1 - использует созданную там БД и таблицу
    """
    # Шаг 1: Проверяем, что задание 1 выполнено
    check_result = ensure_task1_completed()
    if not check_result['success']:
        return check_result
    # Шаг 2: Подключаемся к БД из задания 1
    try:
        conn = sqlite3.connect('lab7.db')
        cursor = conn.cursor()
        print("Используем БД 'lab7.db' из задания 1")
        # Шаг 3: Показываем текущее состояние (до удаления)
        print("\nТЕКУЩЕЕ СОСТОЯНИЕ ТАБЛИЦЫ 'users' (из задания 1):")
        cursor.execute("SELECT * FROM users ORDER BY id")
        current_users = cursor.fetchall()
        print(f"{'ID':<4} {'Имя':<20} {'Email':<25}")
        print("-" * 50)
        for user in current_users:
            print(f"{user[0]:<4} {user[1]:<20} {user[2]:<25}")
        # Шаг 4: Ищем запись для удаления
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        record_to_delete = cursor.fetchone()
        if not record_to_delete:
            available_ids = [str(user[0]) for user in current_users]
            conn.close()
            return {
                'success': False,
                'error': f'Запись с ID={user_id} не найдена',
                'available_ids': available_ids,
                'current_users': len(current_users),
                'note': 'Эти записи были созданы в задании 1'
            }
        # Шаг 5: Удаляем запись (основная задача задания 5)
        print(f"\nУДАЛЕНИЕ ЗАПИСИ ИЗ ЗАДАНИЯ 1:")
        print(f"   ID: {record_to_delete[0]}")
        print(f"   Имя: {record_to_delete[1]}")
        print(f"   Email: {record_to_delete[2]}")
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        rows_deleted = cursor.rowcount
        if rows_deleted > 0:
            conn.commit()
            # Шаг 6: Показываем результат
            print(f"\nЗАПИСЬ УДАЛЕНА:")
            print(f"   Удалено записей: {rows_deleted}")
            # Показываем новое состояние
            cursor.execute("SELECT * FROM users ORDER BY id")
            remaining_users = cursor.fetchall()
            print(f"\nНОВОЕ СОСТОЯНИЕ ТАБЛИЦЫ 'users':")
            print(f"{'ID':<4} {'Имя':<20} {'Email':<25}")
            print("-" * 50)
            for user in remaining_users:
                print(f"{user[0]:<4} {user[1]:<20} {user[2]:<25}")
            conn.close()
            return {
                'success': True,
                'message': f'Запись с ID={user_id} удалена',
                'rows_affected': rows_deleted,
                'deleted_record': {
                    'id': record_to_delete[0],
                    'name': record_to_delete[1],
                    'email': record_to_delete[2]
                },
                'remaining_records': len(remaining_users),
                'remaining_ids': [user[0] for user in remaining_users],
                'connection': 'Использована БД из задания 1'
            }
        else:
            conn.close()
            return {'success': False, 'error': 'Не удалось удалить запись'}
    except sqlite3.Error as e:
        return {'success': False, 'error': f'Ошибка SQLite: {e}'}
def demonstrate_connection():
    """Демонстрация связи между заданиями 1 и 5"""
    print("="*60)
    print("ДЕМОНСТРАЦИЯ СВЯЗИ: ЗАДАНИЕ 5 (удаление) - ЗАДАНИЕ 1 (создание)")
    print("="*60)
    # Проверяем выполнение задания 1
    print("\n1. Проверяем выполнение задания 1...")
    check = ensure_task1_completed()
    if not check['success']:
        print(f"Ошибка: {check['error']}")
        print(f"   Требуемое действие: {check.get('action_required', 'Неизвестно')}")
        return
    print("Задание 1 выполнено, можно выполнять задание 5")
    # Выполняем удаление
    print("\n2. Выполняем задание 5 (удаление записи)...")
    result = delete_record(2)  # Удаляем запись с ID=2
    print(f"\n3. Результат задания 5:")
    print(f"   Успешно: {result['success']}")
    if result['success']:
        print(f"   Сообщение: {result['message']}")
        print(f"   Удалено записей: {result['rows_affected']}")
        print(f"   Осталось записей: {result['remaining_records']}")
        print(f"   Использована БД: {result.get('connection', 'Не указано')}")
    else:
        print(f"   Ошибка: {result['error']}")
    print("\n" + "="*60)
    print("СВЯЗЬ ДОКАЗАНА: Задание 5 работает с результатами задания 1")
    print("="*60)
def create_test_data_if_needed():
    """
    Автоматическое создание тестовых данных из задания 1
    если они отсутствуют (для удобства тестирования)
    """
    if not os.path.exists('lab7.db'):
        print("Создаем БД из задания 1...")
        from N1 import create_sqlite_db
        return create_sqlite_db()
    return {'success': True, 'message': 'БД уже существует'}
if __name__ == "__main__":
    print("Задание 5: Удалить запись (связь с заданием 1)")
    # Создаем тестовые данные, если их нет
    print("Проверяем наличие данных из задания 1...")
    test_result = create_test_data_if_needed()
    if test_result['success']:
        print("Данные из задания 1 готовы")
        # Демонстрация связи
        demonstrate_connection()
        # Примеры использования
        print("\nПримеры использования:")
        # Пример 1: Удаление существующей записи
        print("\n1. Удаление записи с ID=2 (существующей):")
        result1 = delete_record(2)
        print(f"   Результат: {result1.get('message', result1.get('error'))}")
        # Пример 2: Попытка удаления несуществующей записи
        print("\n2. Попытка удаления записи с ID=999 (не существующей):")
        result2 = delete_record(999)
        print(f"   Результат: {result2.get('error', result2.get('message'))}")
        # Пример 3: Показываем оставшиеся записи
        print("\n3. Проверка оставшихся записей:")
        conn = sqlite3.connect('lab7.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"   Всего записей в БД 'lab7.db': {count}")
    else:
        print(f"Ошибка: {test_result.get('error', 'Неизвестная ошибка')}")