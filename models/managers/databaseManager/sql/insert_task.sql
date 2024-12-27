INSERT INTO tasks (number, user_id, title, description)
VALUES (
    COALESCE((SELECT MAX(number) + 1 FROM tasks WHERE user_id = ?), 1), -- Вычисление number
    ?, ?, ? -- Передача user_id, title, description
);
