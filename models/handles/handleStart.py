from pyrogram.types import Message
from models.managers.stateManager import StateManager
from models.keyboards import Keyboards
from models.managers.databaseManager.databaseManager import DatabaseManager


class HandleStart:
    @staticmethod
    def start(telegram_id: int, message: Message):
        """Обрабатывает команду /start."""
        # Проверяем, зарегистрирован ли пользователь
        user = DatabaseManager.make_query([("get_user_by_telegram_id", (telegram_id,))])

        if user:
            # Если пользователь зарегистрирован, приветствуем его
            keyboards = Keyboards.main_menu()
            name = user[0][0]['name']
            message.reply_text(f"Добро пожаловать назад, {name}!", reply_markup=keyboards)
        else:
            # Если не зарегистрирован, просим ввести имя
            message.reply_text("Добро пожаловать! Пожалуйста, введите своё имя для регистрации.")
            StateManager.set_state(telegram_id, "awaiting_name")
