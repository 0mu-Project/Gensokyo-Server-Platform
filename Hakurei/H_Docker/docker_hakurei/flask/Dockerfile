FROM 0muproject/0mu-docker
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
MAINTAINER 0muproject/0mu-flask
ADD requirements.txt /tmp/requirements.txt
RUN curl -s https://bootstrap.pypa.io/get-pip.py | pypy3
RUN pypy3 -m pip install -r /tmp/requirements.txt
EXPOSE 8510
