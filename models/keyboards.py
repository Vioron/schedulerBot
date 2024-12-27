from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from math import ceil


class Keyboards:
    @staticmethod
    def _generate_buttons(total_buttons: int, buttons_per_row: int):
        """
        Приватный метод для генерации кнопок с числами для меню.

        :param total_buttons: Общее количество кнопок.
        :param buttons_per_row: Количество кнопок в одном ряду.
        :return: Список кнопок для меню.
        """
        return [
            [
                InlineKeyboardButton(str(i), callback_data=f"task_number={i}")
                for i in range(row * buttons_per_row + 1, min(total_buttons + 1, row * buttons_per_row + buttons_per_row + 1))
            ]
            for row in range(ceil(total_buttons / buttons_per_row))
        ]

    @staticmethod
    def main_menu():
        """
        Возвращает основное меню.

        :return: InlineKeyboardMarkup
        """
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Список моих задач", callback_data="tasks_list")],
            [InlineKeyboardButton("Создать новую задачу", callback_data="create_task")]
        ])

    @staticmethod
    def all_tasks_menu(total_buttons: int, buttons_per_row: int = 8):
        """
        Возвращает меню с числовыми кнопками и кнопкой "Вернуться в главное меню".

        :param total_buttons: Общее количество кнопок.
        :param buttons_per_row: Количество кнопок в одном ряду (по умолчанию 8).
        :return: InlineKeyboardMarkup
        """
        buttons = Keyboards._generate_buttons(total_buttons, buttons_per_row)
        # Добавляем кнопку "Вернуться в главное меню" в конец
        buttons.append([InlineKeyboardButton("Вернуться в главное меню", callback_data="main_menu")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def task_menu(task_id: int):
        """
        Создаёт меню для управления задачей.

        :param task_id: ID задачи.
        :return: InlineKeyboardMarkup
        """
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Изменить название", callback_data=f"edit_title={task_id}")],
            [InlineKeyboardButton("Изменить описание", callback_data=f"edit_description={task_id}")],
            [InlineKeyboardButton("Удалить задачу", callback_data=f"delete_task={task_id}")],
            [InlineKeyboardButton("Изменить статус", callback_data=f"edit_status={task_id}")],
            [InlineKeyboardButton("⬅️ Вернуться в список задач", callback_data="tasks_list")]
        ])