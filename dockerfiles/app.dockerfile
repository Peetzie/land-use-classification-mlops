FROM python:3.9-slim

EXPOSE $PORT

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY project/ project/
COPY app/main.py main.py
COPY requirements.txt requirements.txt

RUN pip install fastapi
RUN pip install pydantic
RUN pip install uvicorn
RUN --mount=type=cache,target=~/pip/.cache pip install -r requirements.txt --no-cache-dir

CMD exec uvicorn main:app --port $PORT --host 0.0.0.0 --workers 1