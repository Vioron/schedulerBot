-- schema.sql

-- Включение поддержки внешних ключей
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS users;

-- Создание таблицы users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL
);

-- Создание таблицы statuses
CREATE TABLE IF NOT EXISTS statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT UNIQUE NOT NULL
);

-- Добавить статусы в таблицу
INSERT INTO statuses (status) VALUES ('в процессе'), ('отложена'), ('завершена');

-- Создание таблицы tasks
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_id INTEGER DEFAULT 1, -- Ссылка на таблицу статусов
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES statuses (id) ON DELETE SET DEFAULT
);
