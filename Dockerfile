FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

ARG PYTHON_VERSION='3.12.0'
ARG REQUIRED_PACKAGES='make wget build-essential openssl libssl-dev zlib1g-dev'

RUN apt-get update -y
RUN apt-get install -y $REQUIRED_PACKAGES
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz -O Python-$PYTHON_VERSION.tgz
RUN tar xvf Python-$PYTHON_VERSION.tgz && \
    cd Python-$PYTHON_VERSION && \
    ./configure --prefix=/opt/python/$PYTHON_VERSION && \
    make && \
    make install
RUN ln -s /opt/python/$PYTHON_VERSION/bin/python3 /usr/bin/python3
RUN rm /Python-$PYTHON_VERSION.tgz && \
    rm /Python-$PYTHON_VERSION -rdf
RUN apt-get remove -y $REQUIRED_PACKAGES
RUN apt-get clean

WORKDIR /usr/src/app