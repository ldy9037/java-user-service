FROM python:3-slim

WORKDIR /usr/src/
RUN apt update -y
RUN apt -y install libmariadb-dev build-essential
COPY . .

EXPOSE 8000