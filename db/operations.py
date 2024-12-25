import sqlite3
from pyrogram.types import Message, CallbackQuery
from db.manager import Manager
from db.mainMenu import main_menu

class Operations:

    def __init__(self, db_path="db/users.db"):
        self.db_path = db_path
        self.myManager = Manager(db_path)

    def create_tables(self):
        """Создать таблицы, используя файл схемы."""
        with self.myManager.get_db_connection() as conn:
            cursor = conn.cursor()
            with open("db/sql/tables.sql", "r", encoding="utf-8") as f:
                sql_script = f.read()  # Чтение SQL-скрипта
            cursor.executescript(sql_script)  # Выполнение всех SQL-запросов
            conn.commit()

    def start(self, telegram_id: int, message: Message):
        # Открываем новое соединение


        with self.myManager.get_db_connection() as conn:
            cursor = conn.cursor()

            #cursor.execute("DELETE FROM users")
            # Проверяем, зарегистрирован ли пользователь
            cursor.execute("SELECT name FROM users WHERE telegram_id = ?", (telegram_id,))
            user = cursor.fetchone()

            if user:
                # Если пользователь зарегистрирован, приветствуем его
                message.reply_text(f"Добро пожаловать назад, {user['name']}!", reply_markup=main_menu)
            else:
                # Если не зарегистрирован, просим ввести имя
                message.reply_text("Добро пожаловать! Пожалуйста, введите своё имя для регистрации.")
                self.myManager.set_state(telegram_id, "awaiting_name")

    def handle_text(self, telegram_id: int, message: Message):
        """
        Обработчик текстовых сообщений.
        """
        state = self.myManager.get_state(telegram_id)

        if state == "awaiting_name":
            name = message.text.strip()
            self.myManager.set_state(telegram_id, "awaiting_login", {"name": name})
            message.reply_text("Спасибо! Теперь введите уникальный логин.")
        elif state == "awaiting_login":
            login = message.text.strip()
            state_data = self.myManager.get_state_data(telegram_id)
            name = state_data.get("name")

            # Сохраняем пользователя в базу данных
            try:
                with self.myManager.get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO users (telegram_id, name, login) VALUES (?, ?, ?)",
                        (telegram_id, name, login),
                    )
                    conn.commit()

                message.reply_text("Регистрация завершена! Теперь вы можете пользоваться ботом.", reply_markup=main_menu)
                self.myManager.clear_state(telegram_id)
            except sqlite3.IntegrityError:
                message.reply_text("Этот логин уже используется. Пожалуйста, выберите другой.")
        elif state == "awaiting_new_task":
            text_message = message.text.strip()
            with self.myManager.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
                    (telegram_id, text_message, text_message)  # Заполняем title и description одинаковым текстом
                )
            conn.commit()
            message.reply_text("Отлично! Новая задача добавлена в общий список!", reply_markup=main_menu)
        else:
            message.reply_text("Я не понял вашего сообщения. Используйте /start для начала.")

    def handle_callback(self, telegram_id: int, callback_query: CallbackQuery):
        """
        Обработчик inline-кнопок.
        """
        data = callback_query.data

        if data == "option_1":
            with self.myManager.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (telegram_id,))
            conn.commit()
            rows = cursor.fetchall()
            result = "\n\n".join(
                f"ID: {row['id']}\n"
                f"User ID: {row['user_id']}\n"
                f"Title: {row['title']}\n"
                f"Description: {row['description']}\n"
                f"Created At: {row['created_at']}\n"
                f"Status ID: {row['status_id']}"
                for row in rows
            )
            callback_query.message.edit_text(f"Все ваши задачи: {result}", reply_markup=main_menu)
        elif data == "option_2":
            callback_query.message.edit_text("Введите новую задачу: ")
            self.myManager.set_state(telegram_id, "awaiting_new_task")



        else:
            callback_query.answer("Неизвестная опция.", show_alert=True)

