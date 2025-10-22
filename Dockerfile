FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
# Make /app the default Python import root
ENV PYTHONPATH=/app

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pytest --maxfail=1 --disable-warnings -q