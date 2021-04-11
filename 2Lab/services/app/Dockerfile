FROM python:3.9.1-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  pip install --upgrade pip && \
  apt install --no-install-recommends gcc -y && \
  rm -rf /var/lib/apt/lists/*
COPY ./*.py requirements.txt /app/
RUN pip install -r requirements.txt
