from pyrogram.types import Message
from models.managers.stateManager.stateManager import StateManager
from models.keyboards import Keyboards
from models.managers.databaseManager.databaseManager import DatabaseManager
from typing import Union, Dict


class HandleText:
    """
    Класс для обработки текстовых сообщений Telegram-бота.
    """

    @staticmethod
    def awaiting_name(telegram_id: int, name: str, message: Message) -> None:
        """
        Обрабатывает состояние ожидания имени.

        :param telegram_id: ID пользователя в Telegram.
        :param name: Имя пользователя.
        :param message: Сообщение от пользователя.
        """
        StateManager.set_state(telegram_id, "awaiting_login", {"name": name})
        reply_text: str = "Спасибо! Теперь введите уникальный логин."
        message.reply_text(reply_text)

    @staticmethod
    def awaiting_login(telegram_id: int, login: str, message: Message) -> None:
        """
        Обрабатывает состояние ожидания логина.

        :param telegram_id: ID пользователя в Telegram.
        :param login: Логин пользователя.
        :param message: Сообщение от пользователя.
        """
        state_data: Dict[str, Union[str, int]] = StateManager.get_state_data(telegram_id)
        name: str = state_data.get("name")

        try:
            DatabaseManager.make_query([("insert_user", (telegram_id, name, login))])
            keyboard = Keyboards.main_menu()
            reply_text: str = "Регистрация завершена! Теперь вы можете пользоваться ботом."
            message.reply_text(reply_text, reply_markup=keyboard)
            StateManager.clear_state(telegram_id)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                reply_text: str = "Этот логин уже используется. Пожалуйста, выберите другой."
                message.reply_text(reply_text)
            else:
                reply_text: str = "Произошла ошибка. Попробуйте снова позже."
                message.reply_text(reply_text)

    @staticmethod
    def awaiting_new_task_title(telegram_id: int, task_title: str, message: Message) -> None:
        """
        Обрабатывает состояние ожидания новой задачи.

        :param telegram_id: ID пользователя в Telegram.
        :param task_title: Название новой задачи.
        :param message: Сообщение от пользователя.
        """
        StateManager.set_state(telegram_id, "awaiting_new_task_description", {"task_title": task_title})
        reply_text: str = "Введите описание новой задачи:"
        message.reply_text(reply_text)

    @staticmethod
    def awaiting_new_task_description(telegram_id: int, task_description: str, message: Message) -> None:
        """
        Обрабатывает состояние ожидания новой задачи.

        :param telegram_id: ID пользователя в Telegram.
        :param task_description: Описание новой задачи.
        :param message: Сообщение от пользователя.
        """
        state_data: Dict[str, Union[str, int]] = StateManager.get_state_data(telegram_id)
        task_title: str = state_data.get("task_title")
        DatabaseManager.make_query([("insert_task", (telegram_id, telegram_id, task_title, task_description))])
        keyboard = Keyboards.main_menu()
        reply_text: str = "Отлично! Новая задача добавлена в общий список!"
        message.reply_text(reply_text, reply_markup=keyboard)
        StateManager.clear_state(telegram_id)

    @staticmethod
    def enter_new_name_for_task(telegram_id: int, new_title: str, message: Message) -> None:
        """
        Обрабатывает состояние ожидания изменения названия задачи.

        :param telegram_id: ID пользователя в Telegram.
        :param new_title: Новое название задачи.
        :param message: Сообщение от пользователя.
        """
        state_data: Dict[str, Union[str, int]] = StateManager.get_state_data(telegram_id)
        task_number: int = state_data.get("task_number")
        DatabaseManager.make_query([("edit_title_task", (new_title, telegram_id, task_number))])
        keyboard = Keyboards.main_menu()
        reply_text: str = f"Вы изменили название задачи {task_number}"
        message.reply_text(reply_text, reply_markup=keyboard)
        StateManager.clear_state(telegram_id)

    @staticmethod
    def enter_new_description_for_task(telegram_id: int, new_description: str, message: Message) -> None:
        """
        Обрабатывает состояние ожидания изменения описания задачи.

        :param telegram_id: ID пользователя в Telegram.
        :param new_description: Новое описание задачи.
        :param message: Сообщение от пользователя.
        """
        state_data: Dict[str, Union[str, int]] = StateManager.get_state_data(telegram_id)
        task_number: int = state_data.get("task_number")
        DatabaseManager.make_query([("edit_description_task", (new_description, telegram_id, task_number))])
        keyboard = Keyboards.main_menu()
        reply_text: str = f"Вы изменили описание задачи {task_number}"
        message.reply_text(reply_text, reply_markup=keyboard)
        StateManager.clear_state(telegram_id)
