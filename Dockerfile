FROM python:3.11-slim
ENV BOT_NAME=Hrundel
WORKDIR /usr/src/app/${BOT_NAME}
COPY requirements.txt /usr/src/app/${BOT_NAME}
RUN pip install -r /usr/src/app/${BOT_NAME}/requirements.txt
RUN apt update && apt install -y iputils-ping
COPY . /usr/src/app/${BOT_NAME}
