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

ARG CONFIG_PATH
ENV CONFIG_PATH=$CONFIG_PATH

# Check if CONFIG_PATH is empty and set default entry point accordingly
ENTRYPOINT [ "sh", "-c", "if [ -z \"$CONFIG_PATH\" ]; then exec python -u project/train_model.py; else exec python -u project/train_model.py --config \"$CONFIG_PATH\"; fi" ]
