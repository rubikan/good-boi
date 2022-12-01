FROM python:3.11-alpine

RUN apk update && \
    apk add --virtual .voice-build-deps build-base libffi-dev libsodium-dev && \
    apk add gcc bash ffmpeg libffi libsodium libc-dev opus-dev --no-cache && \
    python -m pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    apk del .voice-build-deps

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

COPY . .
CMD ["python", "bot.py"]
