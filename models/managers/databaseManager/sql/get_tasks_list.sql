SELECT
    number, title, description, created_at, status
FROM
    tasks
JOIN
    statuses
ON
    tasks.status_id = statuses.id
WHERE
    user_id = ?