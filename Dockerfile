FROM python:3.9-slim-buster

LABEL maintainer="xq_work@outlook.com"

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

ENV PYTHONUNBUFFERED=1
ENV GROUP_ID=1000 \
    USER_ID=1000

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt
