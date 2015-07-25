FROM python:3.5-slim

RUN mkdir -p /code
WORKDIR /code/

RUN pip install -U pip

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
