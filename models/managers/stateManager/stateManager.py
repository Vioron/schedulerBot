from typing import Dict, Optional, Union


class StateManager:
    user_states: Dict[int, Dict[str, Union[str, int]]] = {}

    @classmethod
    def set_state(cls, user_id: int, state: str, data: Optional[Dict[str, Union[str, int]]] = None) -> None:
        """
        Устанавливает состояние пользователя.

        :param user_id: ID пользователя.
        :param state: Название состояния.
        :param data: Дополнительные данные, связанные с состоянием.
        """
        data_placeholder: Dict[str, Union[str, int]] = data or {}
        cls.user_states[user_id] = {"state": state, "data": data_placeholder}

    @classmethod
    def get_state(cls, user_id: int) -> Optional[str]:
        """
        Возвращает текущее состояние пользователя.

        :param user_id: ID пользователя.
        :return: Текущее состояние пользователя или None, если состояния нет.
        """
        return cls.user_states.get(user_id, {}).get("state")

    @classmethod
    def get_state_data(cls, user_id: int) -> Dict[str, Union[str, int]]:
        """
        Возвращает дополнительные данные состояния пользователя.

        :param user_id: ID пользователя.
        :return: Словарь с данными состояния или пустой словарь, если данных нет.
        """
        return cls.user_states.get(user_id, {}).get("data", {})

    @classmethod
    def clear_state(cls, user_id: int) -> None:
        """
        Очищает состояние пользователя.

        :param user_id: ID пользователя.
        """
        cls.user_states.pop(user_id, None)
