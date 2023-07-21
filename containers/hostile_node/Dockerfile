# Use the appropriate base image for your application
FROM alpine:latest

# Metadata labels
LABEL version="1.0" 
LABEL license="MIT"
LABEL maintainer="guillermo.leiro@estudiantes.uva.es"
LABEL description="Docker container to emulate hostile actions"

### Hostile ###

# Install necessary packages
RUN apk update && apk add \
    python3 \
    py3-pip \
    python3-dev \
    py3-virtualenv \
    curl \
    build-base \
    linux-headers \
    git \
    bash \
    openssh \
    openrc \
    net-tools \
    nmap \
    psmisc \
    traceroute


# Copy user_actions_scripts directory to the container
COPY user_actions_scripts /user_actions_scripts

# Add a directory to PATH
ENV PATH="/user_actions_scripts:${PATH}"

# Grant execute permissions to scripts
RUN chmod +x /user_actions_scripts/*

# Creating virtual python virtual environtment
RUN python3 -m venv /dorothea_venv

# Copy requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN /dorothea_venv/bin/pip3 install -r requirements.txt

# Copy node_daemon.py script
COPY node_daemon.py node_daemon.py

# Set environment variables
ENV RABBITMQ_HOST=localhost
ENV RABBITMQ_QUEUE=rabbit_queue

# Start the application
CMD source /dorothea_venv/bin/activate && /dorothea_venv/bin/python3 node_daemon.py ${RABBITMQ_HOST} ${RABBITMQ_QUEUE}