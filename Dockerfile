# nginx-gunicorn-flask

FROM ubuntu:latest
MAINTAINER Hiller Liao <hillerliao@163.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3.9 python3-pip python3-virtualenv

# Setup flask application
RUN mkdir -p /app
COPY . /app
RUN pip install -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN pip install gunicorn
# RUN pip install git+https://github.com/getsyncr/notion-sdk.git

WORKDIR /app

# Start processes
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:5000"]

