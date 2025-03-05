
# BookSeller API

Этот проект представляет собой API на веб-фреймворке FastAPI для управления продавцами (sellers) и их книгами (books). Данные хранятся в PostgreSQL, а для контейнеризации используется Docker.

## Структура проекта

```
fastapi_shad_task/
│── .vscode/                # Настройки VS Code
│── docker/postgres/        # Файлы для настройки БД
│   ├── create_databases.sql
│   ├── Dockerfile
│── src/                    # Пакеты проекта
│   ├── configurations/     # Конфигурации
│   │   ├── __init__.py
│   │   ├── database.py     # Подключение к БД
│   │   ├── settings.py     # Конфигурация приложения
│   ├── models/             # Описание моделей SQLAlchemy
│   │   ├── __init__.py
│   │   ├── base.py         
│   │   ├── books.py        
│   │   ├── sellers.py
│   ├── routers/            # Роутеры API
│   │   ├── v1/             
│   │   │   ├── __init__.py
│   │   │   ├── books.py    # Эндпоинты для книг
│   │   │   ├── sellers.py  # Эндпоинты для продавцов
│   │   ├── __init__.py
│   ├── schemas/            # Схемы Pydantic
│   │   ├── __init__.py
│   │   ├── books.py
│   │   ├── sellers.py
│   ├── tests/              # Тесты
│   │   ├── __init__.py
│   │   ├── conftest.py     # Фикстуры для тестов
│   │   ├── test_books.py   # Тесты книг
│   │   ├── test_sellers.py # Тесты продавцов
│   ├── __init__.py
│   ├── main.py             # Точка входа в приложение
│   ├── pytest.ini          # Настройки Pytest
│── .env.example            # Пример файла с переменными окружения
│── .gitignore              # Исключения для Git
│── api_tests.http          # HTTP-запросы для тестирования API
│── docker-compose.yml      # Конфигурация Docker Compose
│── requirements.txt        # Зависимости Python
│── README.md               # Описание проекта
```

## 🚀 Запуск проекта

1. **Склонировать репозиторий:**
   ```sh
   git clone https://github.com/OrlovAlexandr/fastapi_shad_task.git
   cd fastapi_shad_task
   ```

2. **Создать и настроить `.env` файл:**
   ```sh
   cp .env.example .env
   ```
   
3. **Установить зависимости:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Запустить проект через Docker Compose:**
   ```sh
   docker-compose up -d --build
   ```

5. **Документация API доступна по адресу:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Запуск тестов

```sh
pytest src/tests
```

## Основные технологии

- **FastAPI** - Веб-фреймворк для API
- **SQLAlchemy** - ORM для работы с PostgreSQL
- **Pydantic** - Валидация данных
- **Docker & Docker Compose** - Контейнеризация
- **Pytest** - Тестирование
