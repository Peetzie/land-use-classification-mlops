# syntax = docker/dockerfile:experimental
FROM python:3.9-slim

EXPOSE $PORT

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean

COPY project/ project/
COPY app/ app/
COPY requirements.txt requirements.txt


RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

CMD exec uvicorn app:app --port $PORT --host 0.0.0.0 --workers 1
