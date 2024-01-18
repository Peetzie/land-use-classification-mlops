# Base image
# syntax = docker/dockerfile:experimental
FROM python:3.9-slim

WORKDIR /

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
COPY project/ project/

COPY Data/ Data/

RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "project/train_model.py"]
