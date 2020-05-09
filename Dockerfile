FROM python:3.7-slim-buster

LABEL maintainer=cong

RUN apt-get -y update && rm -rf /var/lib/apt/lists/*

RUN pip install pandas && rm -rf /root/.cache
RUN mkdir /opt/program

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY preprocessing.py /opt/program
WORKDIR /opt/program