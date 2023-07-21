FROM alpine:latest

# Metadata labels
LABEL version="1.0" 
LABEL license="MIT"
LABEL maintainer="guillermo.leiro@estudiantes.uva.es"
LABEL description="Docker container to export netflows"

### Exporter ###

# Install netflowd as netflow exporter
RUN apk update && apk add softflowd

# Interface to monitor for traffic
ENV INTERFACE=docker0

# Collector server and port for exporting the netflows
ENV SERVER_PORT=localhost:9555

# Netflow version to generate the netflows with (10=IPFIX)
ENV NF_VERSION=10

EXPOSE 9555

CMD softflowd -i ${INTERFACE} -v ${NF_VERSION} -n ${SERVER_PORT} -d