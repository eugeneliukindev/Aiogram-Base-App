FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.1.3"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry lock
RUN poetry install --only main

COPY ./app/ ./app/
COPY ./migrations/ ./migrations/
COPY ./scripts/ ./scripts/
COPY ./texts/ ./texts/
COPY ./alembic.ini ./
COPY ./main.py ./


RUN chmod +x scripts/prestart-migrations.sh
RUN chmod +x scripts/run

ENTRYPOINT ["./scripts/prestart-migrations.sh"]
CMD ["./scripts/run"]