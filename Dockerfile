FROM python:3.8

COPY ./src src
COPY ./resources /resources
COPY ./requirements.txt ./

RUN pip install -r requirements.txt
