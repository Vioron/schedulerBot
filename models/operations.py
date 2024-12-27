from pyrogram.types import Message, CallbackQuery
from models.managers.stateManager import StateManager
from models.managers.databaseManager.databaseManager import DatabaseManager
from models.handles.handleText import HandleText
from models.handles.handleCallback import HandleCallback
from models.handles.handleStart import HandleStart


class Operations:
    @staticmethod
    def initialize_database():
        DatabaseManager.make_query('initialize_database')

    @staticmethod
    def processing_start(telegram_id: int, message: Message):
        """Обрабатывает команду /start."""
        HandleStart.start(telegram_id, message)

    @staticmethod
    def processing_text(telegram_id: int, message: Message):
        """Обработчик текстовых сообщений."""
        state = StateManager.get_state(telegram_id)
        text = message.text.strip()

        if state == "awaiting_name":
            HandleText.awaiting_name(telegram_id, text, message)
        elif state == "awaiting_login":
            HandleText.awaiting_login(telegram_id, text, message)
        elif state == "awaiting_new_task_title":
            HandleText.awaiting_new_task_title(telegram_id, text, message)
        elif state == "awaiting_new_task_description":
            HandleText.awaiting_new_task_description(telegram_id, text, message)
        else:
            message.reply_text("Я не понял вашего сообщения. Используйте /start для начала.")

    @staticmethod
    def processing_callback(telegram_id: int, callback_query: CallbackQuery):
        """Обработчик inline-кнопок."""
        data = callback_query.data

        if data == "tasks_list":
            HandleCallback.tasks_list(telegram_id, callback_query)
        elif data == "create_task":
            HandleCallback.create_task(telegram_id, callback_query)
        elif data == "main_menu":
            HandleCallback.set_main_menu(telegram_id, callback_query)
        elif "task_number" in data:
            task_number = int(data.split("=")[1])  # Извлекаем номер задачи
            HandleCallback.task(telegram_id, callback_query, task_number)
        elif "delete_task" in data:
            task_number = int(data.split("=")[1])  # Извлекаем номер задачи
            HandleCallback.delete_task(telegram_id, callback_query, task_number)
        else:
            callback_query.answer("Неизвестная опция.", show_alert=True)
