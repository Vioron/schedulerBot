from pyrogram.types import Message
from models.managers.stateManager import StateManager
from models.keyboards import Keyboards
from models.managers.databaseManager.databaseManager import DatabaseManager


class HandleText:
    @staticmethod
    def awaiting_name(telegram_id: int, name: str, message: Message):
        """Обрабатывает состояние ожидания имени."""
        StateManager.set_state(telegram_id, "awaiting_login", {"name": name})
        message.reply_text("Спасибо! Теперь введите уникальный логин.")

    @staticmethod
    def awaiting_login(telegram_id: int, login: str, message: Message):
        """Обрабатывает состояние ожидания логина."""
        state_data = StateManager.get_state_data(telegram_id)
        name = state_data.get("name")

        # Сохраняем пользователя в базу данных
        try:
            DatabaseManager.make_query([("insert_user", (telegram_id, name, login))])
            keyboard = Keyboards.main_menu()
            message.reply_text("Регистрация завершена! Теперь вы можете пользоваться ботом.", reply_markup=keyboard)
            StateManager.clear_state(telegram_id)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                message.reply_text("Этот логин уже используется. Пожалуйста, выберите другой.")
            else:
                message.reply_text("Произошла ошибка. Попробуйте снова позже.")

    @staticmethod
    def awaiting_new_task_title(telegram_id: int, task_title: str, message: Message):
        """Обрабатывает состояние ожидания новой задачи."""
        StateManager.set_state(telegram_id, "awaiting_new_task_description", {"task_title": task_title})
        message.reply_text("Введите описание новой задачи:")

    @staticmethod
    def awaiting_new_task_description(telegram_id: int, task_description: str, message: Message):
        """Обрабатывает состояние ожидания новой задачи."""
        state_data = StateManager.get_state_data(telegram_id)
        task_title = state_data.get("task_title")

        DatabaseManager.make_query([("insert_task", (telegram_id, telegram_id, task_title, task_description))])

        keyboard = Keyboards.main_menu()
        message.reply_text("Отлично! Новая задача добавлена в общий список!", reply_markup=keyboard)
