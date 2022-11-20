FROM python:3.11-alpine

RUN apk update && apk add gcc bash libc-dev --no-cache &&\
    python -m pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

COPY . .
CMD ["python", "bot.py"]