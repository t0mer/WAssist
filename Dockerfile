FROM techblog/fastapi:latest

LABEL maintainer="tomer.klein@gmail.com"


ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LOG_LEVEL "DEBUG"
ENV TOKEN ""
ENV PHONE_NUMBER_ID ""
ENV VERIFY_TOKEN ""
ENV OPENAI_KEY ""
ENV ALLOWED_NUMBERS = ""

RUN apt update -yqq

RUN apt install -yqq python3-pip && \
    apt install -yqq libffi-dev && \
    apt install -yqq libssl-dev

RUN mkdir -p /app

COPY docker-requirements.txt /tmp

RUN pip3 install -r /tmp/docker-requirements.txt

COPY app /app

WORKDIR /app

ENTRYPOINT ["/usr/bin/python3", "/app/app.py"]