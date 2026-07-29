# snap ruletka

**snap ruletka** - веб приложение, где люди могут поделиться своими картинками и посмотреть другие. За одно своё фото получаешь 5 случайных чужих

##  Стек

- **Язык:** Python 3.11+
- **Фреймворк:** FastAPI
- **База данных:** PostgreSQL 15
- **Кэш / очереди:** Redis
- **Хранилище файлов:** AWS S3 
- **Фронтенд:** React (в будущем, пока просто JS с HTML)
- **Docker** для развёртывания

## Доступные функции

**Регистрация**
**Загрузка фото**
**Перелистывание чужих фото**  
**Ставить лайк**

##  Безопасность и этика

- Все загружаемые изображения очищаются от EXIF-метаданных.
- Пользователь явно соглашается на показ фото другим участникам.


## Запуск локально

1. git clone <ссылка из code>
2. `cd snap-ruletka`
3. `source .venv/bin/activate`
4. `uv pip install requirements.txt -r`
5. `docker compose up -d`
6. `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`
7. `http://localhost:8000/docs` - документация
   `http://localhost:8000` - сайт 
0. скачать uv
1. git clone <ссылка из code>
2. `cd snap-ruletka`
3. `uv venv`
4. `source .venv/bin/activate`
5. `uv pip install requirements.txt -r`
6. `docker compose up -d`
7. `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`
8. `http://localhost:8000/docs` - документация
   `http://localhost:8000` - сайт
   
## Архитектура

```
snapruletka/
├── app/                  # Бэкенд (FastAPI)
│   ├── api/              # Роутеры (auth, photos)
│   ├── models/           # Модели SQLAlchemy
│   ├── schemas/          # Pydantic схемы запросов/ответов
│   ├── services/         # Бизнес-логика (auth, photo, storage)
│   ├── utils/            # Хеширование паролей, JWT
│   ├── config.py         # Настройки из .env
│   ├── database.py       # Подключение к PostgreSQL
│   └── main.py           # Точка входа FastAPI
├── static/               # Статические файлы
├── templates/            # Шаблоны (Jinja2, если используется)
│   ├── index.html
│   └── app.html
├── alembic/              # Миграции БД
├── .env                  # Локальные переменные окружения
├── docker-compose.yml    # PostgreSQL, Redis, MinIO
├── requirements.txt      # Зависимости Python
└── README.md
```
