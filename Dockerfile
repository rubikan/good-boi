FROM python:3.13.1-alpine

RUN apk update && \
    apk add gcc bash libc-dev --no-cache && \
    python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY . .
CMD ["python", "bot.py"]
