import sqlite3


class Manager:

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.user_states = {}

    def set_state(self, user_id, state, data=None):
        """Установить состояние пользователя."""
        self.user_states[user_id] = {"state": state, "data": data or {}}

    def get_state(self, user_id):
        """Получить текущее состояние пользователя."""
        return self.user_states.get(user_id, {}).get("state")

    def get_state_data(self, user_id):
        """Получить дополнительные данные состояния пользователя."""
        return self.user_states.get(user_id, {}).get("data", {})

    def clear_state(self, user_id):
        """Очистить состояние пользователя."""
        if user_id in self.user_states:
            del self.user_states[user_id]

    def get_db_connection(self):
        """Создать новое соединение с базой данных."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Удобный доступ к данным по названию столбцов
        return conn
