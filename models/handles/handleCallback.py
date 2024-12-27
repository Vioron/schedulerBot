from pyrogram.types import CallbackQuery
from models.managers.stateManager import StateManager
from models.keyboards import Keyboards
from models.managers.databaseManager.databaseManager import DatabaseManager


class HandleCallback:
    @staticmethod
    def tasks_list(telegram_id: int, callback_query: CallbackQuery):
        rows = DatabaseManager.make_query([("get_tasks_list", (telegram_id,))])
        result = HandleCallback._format_tasks(rows)
        keyboard = Keyboards.all_tasks_menu(len(rows))
        callback_query.message.edit_text(f"Все ваши задачи:\n\n{result}", reply_markup=keyboard)

    @staticmethod
    def create_task(telegram_id: int, callback_query: CallbackQuery):
        callback_query.message.edit_text("Введите название новой задачи: ")
        StateManager.set_state(telegram_id, "awaiting_new_task_title")

    @staticmethod
    def set_main_menu(telegram_id: int, callback_query: CallbackQuery):
        keyboard = Keyboards.main_menu()
        callback_query.message.edit_text("Отлично, давайте продолжим! Что вас интересует?", reply_markup=keyboard)
        StateManager.set_state(telegram_id, "main_menu")

    @staticmethod
    def task(telegram_id: int, callback_query: CallbackQuery, task_number: int):
        rows = DatabaseManager.make_query([("get_task", (telegram_id, task_number))])
        result = HandleCallback._format_tasks(rows)
        keyboard = Keyboards.task_menu(task_id=task_number)
        callback_query.message.edit_text(f"Ваша задача номер {task_number}:\n\n{result}", reply_markup=keyboard)

    @staticmethod
    def delete_task(telegram_id: int, callback_query: CallbackQuery, task_number: int):
        DatabaseManager.make_query([
            ("delete_task", (telegram_id, task_number)),
            ("update_numbers_tasks", (telegram_id, task_number))
        ])
        keyboard = Keyboards.main_menu()
        callback_query.message.edit_text(f"Ваша задача номер {task_number} успешно удалена!", reply_markup=keyboard)

    @staticmethod
    def _format_tasks(rows: list) -> str:
        """
        Приватный метод для форматирования списка задач.

        :param rows: Список задач, каждая из которых представлена словарём.
        :return: Отформатированная строка со списком задач.
        """
        return "\n\n".join(
            f"\U0001F31F <b>Задача {row['number']}</b>\n"
            f"<b>Название:</b> {row['title']}\n"
            f"<b>Описание:</b> {row['description']}\n"
            f"<b>Добавлена:</b> {row['created_at']}\n"
            f"<b>Статус:</b> {row['status']}"
            for row in rows
        )
