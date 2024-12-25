from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from dotenv import load_dotenv
import os
import sqlite3

from db.operations import Operations


# Загрузка переменных из .env
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Настройка бота
app = Client("schedulerBot",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token
             )

conn = sqlite3.connect("users.db")
cursor = conn.cursor()


# Инициализация менеджера состояний и базы данных
myOperations = Operations()  # Создаем экземпляр класса
myOperations.create_tables()


@app.on_message(filters.command("start"))
def start(client: Client, message: Message) -> None:
    """
    Обработчик команды /start. Регистрирует пользователя, если это первый вход.
    """
    telegram_id = message.from_user.id
    myOperations.start(telegram_id, message)



@app.on_message(filters.text)
def handle_text(client: Client, message: Message) -> None:
    """
    Обработчик текстовых сообщений.
    """
    telegram_id = message.from_user.id
    myOperations.handle_text(telegram_id, message)


@app.on_callback_query()
def handle_callback(client: Client, callback_query: CallbackQuery) -> None:
    telegram_id = callback_query.from_user.id
    myOperations.handle_callback(telegram_id, callback_query)

if __name__ == "__main__":
    app.run()
