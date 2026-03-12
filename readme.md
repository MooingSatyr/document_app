# JSON Document Storage API
## Требования

- Docker
- Docker Compose

## Запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/username/repo.git
cd repo
```

2. Создать `.env` файл:
```dotenv
DATABASE_URL=postgresql+psycopg2://admin:12345678@db:5432/documents
SECRET_KEY=b4c09517c62a39dc2df795800dfd09d5450fb73b8bc8f35a11cd79835ab5fc00
PERIODIC_FETCH_URL=https://catfact.ninja/fact
PERIODIC_FETCH_INTERVAL=30
```

3. Запустить:
```bash
docker-compose up --build
```

4. Открыть Swagger: http://localhost:8000/docs


## Локально без Docker

1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. В `.env` указать:
```dotenv
DATABASE_URL=postgresql+psycopg2://admin:12345678@localhost:5433/documents
```

3. Запустить только БД:
```bash
docker-compose up db -d
```

4. Применить миграции и запустить:
```bash
alembic upgrade head
uvicorn main:app --reload
```