# Сервис анализа отзывов

Прототип для анализа тональности отзывов на **FastAPI** и **SQLAlchemy**.
Управление зависимостями через **Pipenv**.

### 1. Установка зависимостей

```bash
pipenv install fastapi uvicorn sqlalchemy
```

### 2. Запуск
Для запуска сервера разработки используйте pipenv run.

```bash
pipenv run uvicorn main:app --reload
```
Сервис будет доступен по адресу http://127.0.0.1:8000

### 3. Примеры curl-запросов и их ответов

Позитивный отзыв
```bash
curl -X POST "http://127.0.0.1:8000/reviews" \
-H "Content-Type: application/json" \
-d '{"text": "Мне очень нравится ваш новый дизайн! Супер!"}'
```
Ответ
```bash
{
  "id": 1,
  "text": "Мне очень нравится ваш новый дизайн! Супер!",
  "sentiment": "positive",
  "created_at": "2023-10-27T10:30:00.123456"
}
```

Негативный отзыв
```bash
curl -X POST "http://127.0.0.1:8000/reviews" \
-H "Content-Type: application/json" \
-d '{"text": "Поиск не работает, это ужасно"}'
```
Ответ
```bash
{
  "id": 2,
  "text": "Поиск не работает, это ужасно",
  "sentiment": "negative",
  "created_at": "2023-10-27T10:31:00.567890"
}
```

Получение всех негативных отзывов
```bash
curl "http://127.0.0.1:8000/reviews?sentiment=negative"
```
Ответ
```bash
[
  {
    "id": 2,
    "text": "Поиск не работает, это ужасно",
    "sentiment": "negative",
    "created_at": "2023-10-27T10:31:00.567890"
  }
]
```