from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Пример inline-клавиатуры
main_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("Список моих задачи", callback_data="option_1")],
    [InlineKeyboardButton("Создать новую задачу", callback_data="option_2")]
])