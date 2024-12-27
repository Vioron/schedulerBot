from typing import List, Dict
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from math import ceil


class Keyboards:
    @staticmethod
    def _generate_buttons(total_buttons: int, buttons_per_row: int) -> List[List[InlineKeyboardButton]]:
        """
        Приватный метод для генерации кнопок с числами для меню.

        :param total_buttons: Общее количество кнопок.
        :param buttons_per_row: Количество кнопок в одном ряду.
        :return: Список кнопок для меню.
        """
        callback_data_prefix = "task_number="
        return [
            [
                InlineKeyboardButton(
                    str(i),
                    callback_data=f"{callback_data_prefix}{i}"
                )
                for i in range(
                    row * buttons_per_row + 1,
                    min(total_buttons + 1, row * buttons_per_row + buttons_per_row + 1)
                )
            ]
            for row in range(ceil(total_buttons / buttons_per_row))
        ]

    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """
        Возвращает основное меню.

        :return: InlineKeyboardMarkup
        """
        tasks_list_button_text = "Список моих задач"
        tasks_list_callback_data = "tasks_list"
        create_task_button_text = "Создать новую задачу"
        create_task_callback_data = "create_task"

        return InlineKeyboardMarkup([
            [InlineKeyboardButton(tasks_list_button_text, callback_data=tasks_list_callback_data)],
            [InlineKeyboardButton(create_task_button_text, callback_data=create_task_callback_data)]
        ])

    @staticmethod
    def all_tasks_menu(total_buttons: int, buttons_per_row: int = 8) -> InlineKeyboardMarkup:
        """
        Возвращает меню с числовыми кнопками и кнопкой "Вернуться в главное меню".

        :param total_buttons: Общее количество кнопок.
        :param buttons_per_row: Количество кнопок в одном ряду (по умолчанию 8).
        :return: InlineKeyboardMarkup
        """
        back_to_main_menu_text = "Вернуться в главное меню"
        back_to_main_menu_callback_data = "main_menu"

        buttons = Keyboards._generate_buttons(total_buttons, buttons_per_row)
        buttons.append([InlineKeyboardButton(back_to_main_menu_text, callback_data=back_to_main_menu_callback_data)])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def task_menu(task_number: int) -> InlineKeyboardMarkup:
        """
        Создаёт меню для управления задачей.

        :param task_number: Номер задачи.
        :return: InlineKeyboardMarkup
        """
        edit_title_text = "Изменить название"
        edit_title_callback_data = f"edit_title_task={task_number}"
        edit_description_text = "Изменить описание"
        edit_description_callback_data = f"edit_description_task={task_number}"
        delete_task_text = "Удалить задачу"
        delete_task_callback_data = f"delete_task={task_number}"
        edit_status_text = "Изменить статус"
        edit_status_callback_data = f"edit_status_task={task_number}"
        back_to_tasks_list_text = "Вернуться в список задач"
        back_to_tasks_list_callback_data = "tasks_list"

        return InlineKeyboardMarkup([
            [InlineKeyboardButton(edit_title_text, callback_data=edit_title_callback_data)],
            [InlineKeyboardButton(edit_description_text, callback_data=edit_description_callback_data)],
            [InlineKeyboardButton(delete_task_text, callback_data=delete_task_callback_data)],
            [InlineKeyboardButton(edit_status_text, callback_data=edit_status_callback_data)],
            [InlineKeyboardButton(back_to_tasks_list_text, callback_data=back_to_tasks_list_callback_data)]
        ])

    @staticmethod
    def statuses_menu(statuses: List[Dict], buttons_per_row: int = 1) -> InlineKeyboardMarkup:
        """
        Создаёт меню для выбора статуса.

        :param statuses: Список статусов в формате [(id, status)].
        :param buttons_per_row: Количество кнопок в одном ряду (по умолчанию 1).
        :return: InlineKeyboardMarkup
        """
        back_to_main_menu_text = "Вернуться в главное меню"
        back_to_main_menu_callback_data = "main_menu"

        buttons = [
            [
                InlineKeyboardButton(
                    status[1],
                    callback_data=f"set_status_task={status[0]}"
                )
                for status in statuses[row * buttons_per_row: (row + 1) * buttons_per_row]
            ]
            for row in range(ceil(len(statuses) / buttons_per_row))
        ]
        buttons.append([InlineKeyboardButton(back_to_main_menu_text, callback_data=back_to_main_menu_callback_data)])
        return InlineKeyboardMarkup(buttons)
