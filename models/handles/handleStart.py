from pyrogram.types import Message
from models.managers.stateManager.stateManager import StateManager
from models.keyboards import Keyboards
from models.managers.databaseManager.databaseManager import DatabaseManager


class HandleStart:
    @staticmethod
    def start(telegram_id: int, message: Message) -> None:
        """
        Обрабатывает команду /start.

        :param telegram_id: Идентификатор пользователя Telegram.
        :param message: Сообщение от пользователя.
        """
        # Текстовые строки для ответа
        welcome_back_text: str = "Добро пожаловать назад, {name}!"
        welcome_new_user_text: str = "Добро пожаловать! Пожалуйста, введите своё имя для регистрации."

        # Проверяем, зарегистрирован ли пользователь
        user = DatabaseManager.make_query([("get_user_by_telegram_id", (telegram_id,))])

        if user:
            # Если пользователь зарегистрирован, приветствуем его
            keyboards = Keyboards.main_menu()
            name = user[0][0]
            message.reply_text(welcome_back_text.format(name=name), reply_markup=keyboards)
        else:
            # Если не зарегистрирован, просим ввести имя
            message.reply_text(welcome_new_user_text)
            StateManager.set_state(telegram_id, "awaiting_name")
