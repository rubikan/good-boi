FROM ghcr.io/astral-sh/uv:python3.13-alpine

COPY . .

WORKDIR /app
RUN uv sync --locked

CMD ["python", "main.py"]