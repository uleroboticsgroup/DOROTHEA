FROM alpine:latest

# Metadata labels
LABEL version="1.0" 
LABEL license="MIT"
LABEL maintainer="guillermo.leiro@estudiantes.uva.es"
LABEL description="Docker container to collect netflows"

### Collector ###

# Install netflowd as netflow collector
RUN apk update && apk add nfdump

# Port for incoming netflows
ENV PORT=9555

# Directory to dump the netflows
ENV NF_CAPS_STORE_DIR=/nfcaps

EXPOSE 9555

# Running nfcapd, $(extracting IP of interface recieving the netflows)
CMD nfcapd -b $(ip -4 addr show dev eth0 | grep inet | awk '{print $2}' | cut -d'/' -f1) -p ${PORT} -l ${NF_CAPS_STORE_DIR}