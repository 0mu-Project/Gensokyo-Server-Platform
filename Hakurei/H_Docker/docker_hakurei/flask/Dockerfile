FROM 0muproject/0mu-docker
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
MAINTAINER 0muproject/0mu-flask
ADD requirements.txt /tmp/requirements.txt
RUN curl -s https://bootstrap.pypa.io/get-pip.py | pypy3
RUN curl -s https://bootstrap.pypa.io/get-pip.py | python3
RUN pypy3 -m pip install -r /tmp/requirements.txt
RUN apt-get install -y  git
RUN apt-get install -y  fish
RUN apt-get install -y  python3-dev
RUN apt-get install -y openssh-server
RUN mkdir -p  /var/run/sshd /var/log/supervisor
RUN python3 -m pip install psutil
RUN git clone https://github.com/0mu-Project/Gensokyo-Server-Platform /root/Gensokyo-Server-Platform
RUN echo "export VISIBLE=now" >> /etc/profile
RUN mkdir -p /root/.ssh/ && chmod 700 /root/.ssh/
COPY id_rsa.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
EXPOSE 8509 22 
RUN apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"] 

