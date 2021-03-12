#!/bin/sh
FROM alpine

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk update && apk add --update --no-cache curl certbot python3 py-pip bash
RUN pip3 install idna\<2.6 requests==2.25.1 kubernetes boto3==1.17.26 awscli==1.19.26
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY src/*.py /
COPY scripts/*.sh /

ENTRYPOINT ["certbot"]