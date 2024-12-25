from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from dotenv import load_dotenv
import os

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Настройка бота
app = Client("schedulerBot",
             api_id="21032101",
             api_hash="88100080cba1f4a96e52d905beeb6bdc",
             bot_token="7913656235:AAHpLaNFmx4KKVcHhC7nKl8RHkB4JIrJ_gA"
             )

# Пример inline-клавиатуры
main_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("Опция 1", callback_data="option_1")],
    [InlineKeyboardButton("Опция 2", callback_data="option_2")]
])

@app.on_message(filters.command("start"))
def start(client: Client, message: Message) -> None:
    """
    Обработчик команды /start. Показывает главное меню.
    Args:
        client (Client): Экземпляр клиента Pyrogram.
        message (Message): Объект входящего сообщения.
    """
    message.reply_text(
        "Добро пожаловать! Выберите опцию:",
        reply_markup=main_menu
    )

@app.on_callback_query()
def handle_callback(client: Client, callback_query: CallbackQuery) -> None:
    """
    Обработчик inline-кнопок.
    Args:
        client (Client): Экземпляр клиента Pyrogram.
        callback_query (CallbackQuery): Объект callback-запроса.
    """
    data = callback_query.data

    if data == "option_1":
        callback_query.message.edit_text("Вы выбрали Опцию 1.")
    elif data == "option_2":
        callback_query.message.edit_text("Вы выбрали Опцию 2.")
    else:
        callback_query.answer("Неизвестная опция.", show_alert=True)

@app.on_message(filters.text & ~filters.command([]))
def handle_text(client: Client, message: Message) -> None:
    """
    Обработчик текстовых сообщений.

    Args:
        client (Client): Экземпляр клиента Pyrogram.
        message (Message): Объект входящего сообщения.
    """
    message.reply_text("Пожалуйста, выберите опцию сначала, используя /start.")

if __name__ == "__main__":
    app.run()
