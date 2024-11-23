-- Створення таблиці користувачів (users)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                 -- Унікальний ідентифікатор користувача (автоінкрементний ключ)
    fullname VARCHAR(100) NOT NULL,        -- Повне ім'я користувача (обов'язкове поле, довжина до 100 символів)
    email VARCHAR(100) UNIQUE NOT NULL     -- Електронна пошта користувача (обов'язкове поле, значення мають бути унікальними)
);

-- Створення таблиці статусів (status)
CREATE TABLE status (
    id SERIAL PRIMARY KEY,                 -- Унікальний ідентифікатор статусу (автоінкрементний ключ)
    name VARCHAR(50) UNIQUE NOT NULL       -- Назва статусу (обов'язкове поле, значення мають бути унікальними, довжина до 50 символів)
);

-- Створення таблиці завдань (tasks)
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,                 -- Унікальний ідентифікатор завдання (автоінкрементний ключ)
    title VARCHAR(100) NOT NULL,           -- Назва завдання (обов'язкове поле, довжина до 100 символів)
    description TEXT,                      -- Опис завдання (може бути порожнім)
    status_id INTEGER REFERENCES status(id),  -- Зовнішній ключ, що посилається на таблицю статусів (поле id)
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE -- Зовнішній ключ, що посилається на таблицю користувачів (поле id). При видаленні користувача автоматично видаляються його завдання
);

-- 1. Отримати всі завдання певного користувача
SELECT * FROM tasks WHERE user_id = 1;

-- 2. Вибрати завдання за певним статусом
SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус завдання
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 2;

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);

-- 5. Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New Task', 'Task description', (SELECT id FROM status WHERE name = 'new'), 1);

-- 6. Отримати всі завдання, які ще не завершено
SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- 7. Видалити завдання
DELETE FROM tasks WHERE id = 3;

-- 8. Знайти користувачів з певною електронною поштою
SELECT * FROM users WHERE email LIKE '%@example.com';

-- 9. Оновити ім'я користувача
UPDATE users
SET fullname = 'Some Name'
WHERE id = 1;

-- 10. Отримати кількість завдань для кожного статусу
SELECT s.name AS status, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name;

-- 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
SELECT t.*
FROM tasks t
INNER JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';

-- 12. Отримати список завдань, що не мають опису
SELECT * FROM tasks WHERE description IS NULL OR description = '';

-- 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
SELECT u.fullname, t.title
FROM users u
INNER JOIN tasks t ON u.id = t.user_id
WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress');

-- 14. Отримати користувачів та кількість їхніх завдань
SELECT u.fullname, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.fullname;
