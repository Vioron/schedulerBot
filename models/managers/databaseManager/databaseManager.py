import sqlite3
from typing import List, Tuple, Optional, Union


class DatabaseManager:
    db_path = "models/managers/databaseManager/users.db"
    sql_path = "models/managers/databaseManager/sql"

    @classmethod
    def make_query(cls, queries: Union[str, List[Tuple[str, Optional[Tuple]]]]) -> List[Tuple]:
        """
        Выполняет SQL-запросы и возвращает результат.

        :param queries: Либо строка с именем файла SQL-запроса, либо список запросов с параметрами.
        :return: Список результатов (если запросы возвращают данные).
        """
        try:
            with cls._get_db_connection() as conn:
                cursor = conn.cursor()

                if isinstance(queries, str):
                    # Выполнение одиночного запроса из файла
                    sql_script = cls._get_sql_script(f"{cls.sql_path}/{queries}.sql")
                    cursor.executescript(sql_script)
                elif isinstance(queries, list):
                    # Выполнение массива запросов
                    for sql_query, params in queries:
                        sql_script = cls._get_sql_script(f"{cls.sql_path}/{sql_query}.sql")
                        cursor.execute(sql_script, params or ())
                else:
                    raise ValueError("`queries` должен быть строкой или списком запросов с параметрами.")

                conn.commit()

                # Пытаемся получить результат, если запросы возвращают данные
                try:
                    result = cursor.fetchall()
                except sqlite3.ProgrammingError:
                    result = []  # Если запрос не возвращает данные

            return result
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Ошибка выполнения запроса: {e}")

    @classmethod
    def _get_db_connection(cls) -> sqlite3.Connection:
        """
        Получить подключение к базе данных.

        :return: Объект подключения SQLite.
        """
        connection = sqlite3.connect(cls.db_path)
        connection.row_factory = sqlite3.Row  # Позволяет возвращать строки как словари
        return connection

    @classmethod
    def _get_sql_script(cls, file_path: str) -> str:
        """
        Получить SQL-скрипт из файла.

        :param file_path: Путь к файлу с SQL-скриптом.
        :return: Содержимое файла SQL в виде строки.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл с SQL-скриптом '{file_path}' не найден.")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла '{file_path}': {e}")
