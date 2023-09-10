FROM python:3

WORKDIR /app

COPY ./src ./src
COPY ./requirements.txt ./
COPY ./resources ./resources


RUN pip install -r requirements.txt