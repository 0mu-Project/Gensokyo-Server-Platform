FROM ubuntu:14.04
MAINTAINER m85091081@gmail.com

# Let's start with some basic stuff.
RUN apt-get update -qq && apt-get install -qqy \
    apt-transport-https \
    ca-certificates \
    curl \
    lxc \
    iptables \
    supervisor
    
# Install Docker from Docker Inc. repositories.
RUN curl -sSL https://get.docker.com/ | sh

# Install the magic wrapper.
ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker

# Supervisor config
RUN mkdir -p  /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Yakumo-Instance install 
RUN mkdir -p /opt/yakumo-instance
COPY ../../Yakumo/Yakumo-Instance/ /opt/yakumo-instance


# Define additional metadata for our image.
VOLUME /var/lib/docker
CMD ["/usr/bin/supervisord"]

