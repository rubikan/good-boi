FROM python:3.11-slim-buster

RUN apt-get update && apt-get install gcc -y && apt-get clean \
    python -m pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

COPY . .
CMD ["python", "bot.py"]