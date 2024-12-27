from typing import Optional
from pyrogram.types import Message, CallbackQuery
from models.managers.stateManager.stateManager import StateManager
from models.managers.databaseManager.databaseManager import DatabaseManager
from models.handles.handleText import HandleText
from models.handles.handleCallback import HandleCallback
from models.handles.handleStart import HandleStart


class Operations:
    @staticmethod
    def initialize_database() -> None:
        """
        Инициализирует базу данных.
        """
        query_name = "initialize_database"
        DatabaseManager.make_query(query_name)

    @staticmethod
    def processing_start(telegram_id: int, message: Message) -> None:
        """
        Обрабатывает команду /start.

        :param telegram_id: ID пользователя в Telegram.
        :param message: Объект сообщения.
        """
        HandleStart.start(telegram_id, message)

    @staticmethod
    def processing_text(telegram_id: int, message: Message) -> None:
        """
        Обрабатывает текстовые сообщения.

        :param telegram_id: ID пользователя в Telegram.
        :param message: Объект сообщения.
        """
        state = StateManager.get_state(telegram_id)
        text = message.text.strip()

        unknown_message_response = "Я не понял вашего сообщения. Используйте /start для начала."

        if state == "awaiting_name":
            HandleText.awaiting_name(telegram_id, text, message)
        elif state == "awaiting_login":
            HandleText.awaiting_login(telegram_id, text, message)
        elif state == "awaiting_new_task_title":
            HandleText.awaiting_new_task_title(telegram_id, text, message)
        elif state == "awaiting_new_task_description":
            HandleText.awaiting_new_task_description(telegram_id, text, message)
        elif state == "enter_new_name_for_task":
            HandleText.enter_new_name_for_task(telegram_id, text, message)
        elif state == "enter_new_description_for_task":
            HandleText.enter_new_description_for_task(telegram_id, text, message)
        else:
            message.reply_text(unknown_message_response)

    @staticmethod
    def processing_callback(telegram_id: int, callback_query: CallbackQuery) -> None:
        """
        Обрабатывает нажатия inline-кнопок.

        :param telegram_id: ID пользователя в Telegram.
        :param callback_query: Объект callback-запроса.
        """
        data = callback_query.data

        unknown_option_response = "Неизвестная опция."

        if data == "tasks_list":
            HandleCallback.tasks_list(telegram_id, callback_query)
        elif data == "create_task":
            HandleCallback.create_task(telegram_id, callback_query)
        elif data == "main_menu":
            HandleCallback.set_main_menu(telegram_id, callback_query)
        elif "task_number" in data:
            task_number: Optional[int] = int(data.split("=")[1])  # Извлекаем номер задачи
            HandleCallback.select_task(telegram_id, callback_query, task_number)
        elif "edit_title_task" in data:
            task_number: Optional[int] = int(data.split("=")[1])  # Извлекаем номер задачи
            HandleCallback.edit_title_task(telegram_id, callback_query, task_number)
        elif "edit_description_task" in data:
            task_number: Optional[int] = int(data.split("=")[1])  # Извлекаем номер задачи
            HandleCallback.edit_description_task(telegram_id, callback_query, task_number)
        elif "delete_task" in data:
            task_number: Optional[int] = int(data.split("=")[1])  # Извлекаем номер задачи
            HandleCallback.delete_task(telegram_id, callback_query, task_number)
        elif "edit_status_task" in data:
            task_number: Optional[int] = int(data.split("=")[1])  # Извлекаем номер задачи
            HandleCallback.edit_status_task(telegram_id, callback_query, task_number)
        elif "set_status_task" in data:
            status_id: Optional[int] = int(data.split("=")[1])  # Извлекаем ID статуса
            HandleCallback.set_status_task(telegram_id, callback_query, status_id)
        else:
            callback_query.answer(unknown_option_response, show_alert=True)
