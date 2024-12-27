UPDATE tasks
SET number = number - 1
WHERE user_id = ? AND number > ?