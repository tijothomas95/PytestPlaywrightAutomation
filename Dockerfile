FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt