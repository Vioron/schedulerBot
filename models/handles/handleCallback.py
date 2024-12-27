from typing import List, Dict
from pyrogram.types import CallbackQuery
from models.managers.stateManager.stateManager import StateManager
from models.keyboards import Keyboards
from models.managers.databaseManager.databaseManager import DatabaseManager


class HandleCallback:
    """
    Класс для обработки колбэков Telegram-бота.
    """

    @staticmethod
    def tasks_list(telegram_id: int, callback_query: CallbackQuery) -> None:
        """
        Отображает список задач пользователя.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        """
        no_tasks_message = "У вас пока нет задач. Да вы счастливчик!"
        tasks_message = "Все ваши задачи:\n\n{}"

        rows = DatabaseManager.make_query([("get_tasks_list", (telegram_id,))])
        result = HandleCallback._format_tasks(rows)
        keyboard = Keyboards.all_tasks_menu(len(rows))
        text = tasks_message.format(result) if rows else no_tasks_message
        callback_query.message.edit_text(text, reply_markup=keyboard)

    @staticmethod
    def create_task(telegram_id: int, callback_query: CallbackQuery) -> None:
        """
        Устанавливает состояние для создания новой задачи.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        """
        create_task_message = "Введите название новой задачи: "

        callback_query.message.edit_text(create_task_message)
        StateManager.set_state(telegram_id, "awaiting_new_task_title")

    @staticmethod
    def set_main_menu(telegram_id: int, callback_query: CallbackQuery) -> None:
        """
        Возвращает пользователя в главное меню.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        """
        main_menu_message = "Отлично, давайте продолжим! Что вас интересует?"

        keyboard = Keyboards.main_menu()
        callback_query.message.edit_text(main_menu_message, reply_markup=keyboard)
        StateManager.clear_state(telegram_id)

    @staticmethod
    def select_task(telegram_id: int, callback_query: CallbackQuery, task_number: int) -> None:
        """
        Отображает детали выбранной задачи.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        :param task_number: Номер задачи.
        """
        rows = DatabaseManager.make_query([("get_task", (telegram_id, task_number))])
        result = HandleCallback._format_tasks(rows)
        task_message = f"Ваша задача номер {task_number}:\n\n{result}"

        keyboard = Keyboards.task_menu(task_number)
        callback_query.message.edit_text(task_message, reply_markup=keyboard)
        StateManager.clear_state(telegram_id)

    @staticmethod
    def edit_title_task(telegram_id: int, callback_query: CallbackQuery, task_number: int) -> None:
        """
        Устанавливает состояние для изменения названия задачи.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        :param task_number: Номер задачи.
        """
        edit_title_message = f"Введи новое название задачи {task_number}:"

        callback_query.message.edit_text(edit_title_message)
        StateManager.set_state(telegram_id, "enter_new_name_for_task", {"task_number": task_number})

    @staticmethod
    def edit_description_task(telegram_id: int, callback_query: CallbackQuery, task_number: int) -> None:
        """
        Устанавливает состояние для изменения описания задачи.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        :param task_number: Номер задачи.
        """
        edit_description_message = f"Введи новое описание задачи {task_number}:"

        callback_query.message.edit_text(edit_description_message)
        StateManager.set_state(telegram_id, "enter_new_description_for_task", {"task_number": task_number})

    @staticmethod
    def delete_task(telegram_id: int, callback_query: CallbackQuery, task_number: int) -> None:
        """
        Удаляет задачу пользователя.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        :param task_number: Номер задачи.
        """
        delete_task_message = f"Ваша задача номер {task_number} успешно удалена!"

        DatabaseManager.make_query([
            ("delete_task", (telegram_id, task_number)),
            ("update_numbers_tasks", (telegram_id, task_number))
        ])
        keyboard = Keyboards.main_menu()
        callback_query.message.edit_text(delete_task_message, reply_markup=keyboard)
        StateManager.clear_state(telegram_id)

    @staticmethod
    def edit_status_task(telegram_id: int, callback_query: CallbackQuery, task_number: int) -> None:
        """
        Устанавливает состояние для изменения статуса задачи.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        :param task_number: Номер задачи.
        """
        edit_status_message = f"Выберите новый статус для задачи {task_number}:"

        result = DatabaseManager.make_query([("get_statuses", None)])
        keyboard = Keyboards.statuses_menu(result)
        callback_query.message.edit_text(edit_status_message, reply_markup=keyboard)
        StateManager.set_state(telegram_id, "edit_status_task", {"task_number": task_number})

    @staticmethod
    def set_status_task(telegram_id: int, callback_query: CallbackQuery, status_id: int) -> None:
        """
        Устанавливает новый статус для задачи.

        :param telegram_id: ID пользователя Telegram.
        :param callback_query: Объект колбэка.
        :param status_id: ID нового статуса.
        """
        success_status_message = "Статус задачи {} успешно изменён"

        state_data = StateManager.get_state_data(telegram_id)
        task_number = state_data.get("task_number")
        DatabaseManager.make_query([("update_status_tasks", (status_id, telegram_id, task_number))])
        keyboard = Keyboards.main_menu()
        callback_query.message.edit_text(success_status_message.format(task_number), reply_markup=keyboard)
        StateManager.clear_state(telegram_id)

    @staticmethod
    def _format_tasks(rows: List[Dict]) -> str:
        """
        Приватный метод для форматирования списка задач.

        :param rows: Список задач, каждая из которых представлена словарём.
        :return: Отформатированная строка со списком задач.
        """
        task_template = (
            "\U0001F31F <b>Задача {number}</b>\n"
            "<b>Название:</b> {title}\n"
            "<b>Описание:</b> {description}\n"
            "<b>Добавлена:</b> {created_at}\n"
            "<b>Статус:</b> {status}"
        )
        return "\n\n".join(
            task_template.format(
                number=row["number"],
                title=row["title"],
                description=row["description"],
                created_at=row["created_at"],
                status=row["status"]
            ) for row in rows
        )
