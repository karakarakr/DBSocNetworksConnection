#!/bin/bash

# Регистрация нового пользователя
curl -X POST "http://localhost:8000/signin" -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass"
}'

# Авторизация пользователя и получение токена
curl -X POST "http://localhost:8000/login" -H "Content-Type: application/json" -d '{
    "email": "test@example.com",
    "password": "testpass"
}'

# Получение списка всех задач
curl -X GET "http://localhost:8000/tasks" -H "Authorization: Bearer <ACCESS_TOKEN>"

# Добавление новой задачи
curl -X POST "http://localhost:8000/tasks" -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{
    "title": "New Task",
    "description": "This is a new task",
    "social_networks": [
        {
            "soc_network": "Telegram",
            "url": "https://t.me/example",
            "username": "telegramuser",
            "description": "Description of telegram account",
            "followers": 1000,
            "verified": true
        },
        {
            "soc_network": "Instagram",
            "url": "https://instagram.com/example",
            "username": "instauser",
            "description": "Instagram description",
            "followers": 5000,
            "verified": false
        }
    ]
}'

# Получение задачи по ID
curl -X GET "http://localhost:8000/tasks/1" -H "Authorization: Bearer <ACCESS_TOKEN>"

# Обновление задачи по ID
curl -X PUT "http://localhost:8000/tasks/1" -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{
    "title": "Updated Task",
    "description": "Updated description",
    "completed": true
}'

# Удаление задачи по ID
curl -X DELETE "http://localhost:8000/tasks/1" -H "Authorization: Bearer <ACCESS_TOKEN>"