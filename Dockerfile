FROM python:3.10-slim

WORKDIR /home/web-service

COPY . /home/web-service

RUN pip install --no-cache-dir Flask requests
