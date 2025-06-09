[![Python](https://img.shields.io/badge/Python-3.12+-2d91f5?logo=python&logoColor=FFD43B&style=for-the-badge)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-2d91f5?logo=telegram&style=for-the-badge)](https://aiogram.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&style=for-the-badge)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/Postgresql-16.0-2d91f5?logo=postgresql&logoColor=white&style=for-the-badge)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-latest-DC382D?logo=redis&style=for-the-badge)](https://redis.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.11.5-E92063?logo=pydantic&style=for-the-badge)](https://docs.pydantic.dev/latest/)
[![Alembic](https://img.shields.io/badge/Alembic-1.16.1-2d91f5?style=for-the-badge)](https://redis.io/)
[![Poetry](https://img.shields.io/badge/Poetry-2.1.3-2d91f5?logo=poetry&style=for-the-badge)](https://python-poetry.org/)
[![Mypy](https://img.shields.io/badge/Mypy-1.6-2d91f5?logo=python&logoColor=59acff&style=for-the-badge)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/badge/Ruff-0.11.12-green?logo=ruff&style=for-the-badge)](https://docs.astral.sh/ruff/)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-4.2.0-yellow?logo=precommit&style=for-the-badge)](https://pre-commit.com/)
[![Docker](https://img.shields.io/badge/Docker-24.0-2d91f5?logo=docker&style=for-the-badge)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/Pytest-8.4.0-2d91f5?logo=pytest&style=for-the-badge)](https://docs.pytest.org/)
[![LICENSE](https://img.shields.io/badge/license-mit-green?style=for-the-badge)](LICENSE.txt)

# Aiogram Base App 🚀

Легкий и готовый к использованию шаблон для разработки телеграмм бота на [**Aiogram**](https://github.com/aiogram/aiogram). Начните работу за считанные минуты!

---

## 🌟 Почему стоит выбрать этот шаблон?

Этот стартовый набор — ваш быстрый путь к созданию мощных Telegram-ботов с
[**Aiogram**](https://github.com/aiogram/aiogram). Забудьте о:

- 🔧 Рутинной настройки базы данных
- ⚙️ Сложностях с конфигурацией окружения
- 📂 Трате времени на инициализацию проекта и его структуру

---

## ✨ Основные инструменты

- 🛠️ **Типобезопасный код** с [**Mypy**](https://github.com/python/mypy) для надежной проверки типов
- 🧼 **Чистый код** благодаря линтеру и форматтеру [**Ruff**](https://github.com/astral-sh/ruff)
- 📦 **Управление зависимостями** с помощью [**Poetry**](https://github.com/python-poetry/poetry) для удобной работы
- 🗃️ **Высокопроизводительная база данных** с асинхронным [**SQLAlchemy**](https://github.com/sqlalchemy/sqlalchemy) и
  [**Asyncpg**](https://magicstack.github.io/asyncpg/current/) для [**PostgreSQL**](https://www.postgresql.org/)
- 🔄 **Простые миграции базы данных** с [**Alembic**](https://github.com/sqlalchemy/alembic)
- ⚡ **Быстрое кэширование** с [**Redis**](https://github.com/redis/redis-py) для надежного хранения FSM (storage)
- ⚙️ **Управление переменными окружения** с помощью [**Pydantic-settings**](https://github.com/pydantic/pydantic-settings)
- 📁 **Асинхронная работа с файлами** через [**Aiofiles**](https://github.com/Tinche/aiofiles) для эффективной обработки
- 🛡️ **Контроль качества кода** с [**Pre-commit**](https://github.com/pre-commit/pre-commit) хуками и Ruff для чистоты
  ваших коммитов
- ✅ **Тесты** с [**pytest**](https://github.com/pytest-dev/pytest) для тестирования вашего кода
- 🐳 **Docker-образ** для:
    - [**PostgreSQL**](https://hub.docker.com/_/postgres)
    - [**Redis**](https://hub.docker.com/_/redis)

---

## Требования

- 🐍 Python 3.12+
- 📦 [Poetry](https://python-poetry.org/docs/#installation) (*опционально*, для управления зависимостями)
- 🐳 [Docker](https://www.docker.com/get-started) (*опционально*, для запуска **Postgres** и **Redis**)

---

## Установка

### 1. Клонирование репозитория 📥

- Через `HTTPS`:
  ```bash
  git clone https://github.com/eugeneliukindev/Aiogram-Base-App.git
  ```

- Через `SSH` (*рекомендуется*):
   ```bash
   git clone git@github.com:eugeneliukindev/Aiogram-Base-App.git
   ```

## 2. Установка зависимостей ➕

- Через `Poetry` (*рекомендуется*):
  - Полная установка:
    ```bash
    poetry install
    ```
  
  - Установка только main зависимостей:
    ```bash
    poetry install --only main
    ```

- Через `pip`:
  ```bash
  pip install -r requirements.txt
  ```

---

### 3. Настройка переменных окружения 🔑

Замените переменные окружения из [.env-template](.env-template) в `.env`

### 4. Запуск Docker контейнеров 🐳
```bash
docker compose --profile default up -d 
```

### 5. Миграции Alembic 🔄
```bash
alembic upgrade head
```

---

### 6. Запуск Бота 🚀
```bash
python main.py
```

---

## Инструменты для разработки 🛠️

- Выполните `mypy .` для проверки типов
- Выполните `ruff check .` для linting
- Выполните `ruff format .` для форматирования кода
- Выполните `docker compose --profile test up -d` & `pytest` для запуска тестов 

---

## Дополнительно 📌

- **Важное замечание про `.env`** ⚠️

  Файл `.env` используется для хранения конфиденциальных данных, таких как настройки базы данных, токены и т.п. Ради
  примера он не добавлен в `.gitignore`. Для безопасности настоятельно рекомендуется добавить `.env` в `.gitignore`,
  чтобы избежать случайной отправки конфиденциальных данных в репозиторий:
  ```bash
  echo ".env" >> .gitignore
  ```

- **Инициализация pre-commit хуков**

  Если у вас установлены `dev` зависимости Ю вместе с этим был добавлен `pre-commit`, чтобы его активировать нужно:
  ```bash
  pre-commit install
  ```

---

## Вклад в проект 🤝

Мы приветствуем любые улучшения! Чтобы внести вклад:

1. Сделайте форк репозитория
2. Создайте ветку для новой функциональности (`git checkout -b feature/YourFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add YourFeature'`)
4. Отправьте ветку в репозиторий (`git push origin feature/YourFeature`)
5. Откройте Pull Request

---

## Лицензия 📄

Проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE.txt).

---

Удачного кодинга! 🎉 Если у вас есть вопросы или нужна помощь, создайте issue в репозитории.