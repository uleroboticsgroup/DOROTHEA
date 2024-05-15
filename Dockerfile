# Stage 1: (build)
FROM ubuntu:noble as build

# Install required dependencies for building pmacct
RUN apt-get update && \
    apt-get install -y \
        libpcap-dev \
        pkg-config \
        libtool \
        autoconf \
        automake \
        make \
        bash \
        libstdc++-14-dev \
        g++

# Copy pmacct source code into the build stage
COPY pmacct tmp/pmacct

# Set the working directory to the pmacct directory
WORKDIR /tmp/pmacct

# Run autogen.sh, configure, make, and make install to build pmacct
RUN ./autogen.sh && \
    ./configure && \
    make && \
    make install


# Stage 2: Final Image
FROM ubuntu:noble

# Copy the built files from the build stage to the final stage
COPY --from=build /usr/local/ /usr/local

# Install libpcap0.8 package required by pmacct
RUN apt-get update && \
    apt-get install -y \
    libpcap0.8 && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Set the default command to run pmacctd with the specified configuration file
CMD pmacctd -f /dorothea/dorothea-pmacctd.conf