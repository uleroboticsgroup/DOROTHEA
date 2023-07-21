# Use the appropriate base image for your application
FROM alpine:latest

# Metadata labels
LABEL version="1.0" 
LABEL license="MIT"
LABEL maintainer="guillermo.leiro@estudiantes.uva.es"
LABEL description="Docker container to emulate vanilla actions"

### Vanilla ###

# Install packages
RUN apk update && apk add \
    python3 \
    py3-pip \
    py3-virtualenv \
    curl \
    git \
    bash \
    openrc \    
    firefox \
    openssh

# Installing geckodriver
RUN wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin
RUN chmod +x /usr/local/bin/geckodriver
COPY user_actions_scripts /user_actions_scripts

# SSH (new pass: dorothea)
RUN echo 'root:dorothea' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN rc-status
RUN touch /run/openrc/softlevel

# Adding user scripts to PATH
COPY user_actions_scripts /user_actions_scripts
ENV PATH="/user_actions_scripts:${PATH}"
RUN chmod +x /user_actions_scripts/*

# Creating virtual python virtual environtment
RUN python3 -m venv /dorothea_venv

# Installing python requirements
COPY requirements.txt requirements.txt
RUN /dorothea_venv/bin/pip3 install -r requirements.txt

# Copying node daemon
COPY node_daemon.py node_daemon.py

# Rabbit-MQ container/server IP
ENV RABBITMQ_HOST=localhost

# Rabbit-MQ queue name
ENV RABBITMQ_QUEUE=rabbit_queue

CMD source /dorothea_venv/bin/activate && /dorothea_venv/bin/python3 node_daemon.py ${RABBITMQ_HOST} ${RABBITMQ_QUEUE}