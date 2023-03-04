FROM python:3.12.0a5-slim-buster

RUN apt update
RUN python3 -m pip install requests websocket-client

WORKDIR /usr/app/src

COPY . ./