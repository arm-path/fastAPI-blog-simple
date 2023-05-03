## Пример блога на FastAPI
- Регистрация и авторизация пользователя с исползованием [FastAPI Users](https://github.com/frankie567/fastapi-users).
- Добавление и отображение статей.
- Добавление комментарий к статьям.
- Примеры страниц (templates).
- Тесты приложения.

Технологии: 
- Аутентификация пользователей (fastapi-users).
- Отложенные задачи (celery + redis).
- Websockets.
- Templates.
- Pytest.

### Начало работы:
#### 1. Добавить файл ".env" со следущим содержимым:
DB_USER=yourUserDb \
DB_PASSWORD=yourPasswordDb \
DB_HOST=yourHostDb \
DB_NAME=yourNameDb \
DB_USER_TEST=yourTestUserDb\
DB_PASSWORD_TEST=yourTestPasswordDb \
DB_NAME_TEST=yourTestNameDb

SECRET_USER_AUTHENTICATION=secret \
SECRET_USER_MANAGER=secret \
SECRET_EMAIL_CONFIRMATION=secret

SMTP_HOST=yourHostSMTP\
SMTP_PORT=yourPostSMTP\
SMTP_USER=yourUserSMTP\
SMTP_PASSWORD=yourPasswordSMTP 

#### 2. Установить зависимости:
> pip install -r requirements.txt

### 3. Применить миграции:
> alembic revision --autogenerate \
> alembic upgrade head

#### 4. Запустить Celery (Применяется для активации пользователя по электронной почте):
> celery -A src.tasks.task:celery worker --loglevel=INFO -P solo \
> celery -A src.tasks.task:celery flower

#### 5. Запустить сервер FastApi:
> uvicorn src.main:app --reload

#### Тестирование:
> pytest -v -s src/tests

### Инструкции:
Открыть `http://localhost:8000/docs` для просмотра доступных эндпоинтов. \
Примечание: Перед регистрацией пользователя необходимо в базу данных добавить роль.