FROM ubuntu:latest

MAINTAINER 0muproject/0mu-docker-ubuntu-tw
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y curl
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN curl -L https://bitbucket.org/pypy/pypy/downloads/pypy3-2.4.0-linux64.tar.bz2 | tar -jxf - && mv pypy* /opt/pypy3
ENV PATH $PATH:/opt/pypy3/bin

ENV HOME /root

WORKDIR /root
