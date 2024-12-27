class StateManager:
    user_states = {}

    @classmethod
    def set_state(cls, user_id, state, data=None):
        """Установить состояние пользователя."""
        cls.user_states[user_id] = {"state": state, "data": data or {}}

    @classmethod
    def get_state(cls, user_id):
        """Получить текущее состояние пользователя."""
        return cls.user_states.get(user_id, {}).get("state")

    @classmethod
    def get_state_data(cls, user_id):
        """Получить дополнительные данные состояния пользователя."""
        return cls.user_states.get(user_id, {}).get("data", {})

    @classmethod
    def clear_state(cls, user_id):
        """Очистить состояние пользователя."""
        cls.user_states.pop(user_id, None)



