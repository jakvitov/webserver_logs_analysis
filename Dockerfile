FROM python:3.8

COPY ./src src
COPY ./resources /resources
COPY ./requirements.txt ./
COPY ./start_analysis ./

RUN pip install -r requirements.txt