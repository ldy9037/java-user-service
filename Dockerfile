FROM python:3.7-slim as builder
WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    apt install -y libmariadb-dev build-essential 
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.7-slim

WORKDIR /usr/src

RUN apt update && \
    apt install -y libmariadb-dev build-essential 

COPY . .
COPY --from=builder /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

EXPOSE 8000