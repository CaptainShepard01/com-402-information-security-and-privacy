# syntax=docker/dockerfile:latest
FROM docker.io/python:3.12-bookworm AS mitm

# Enable APT package caching
RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# Install required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        build-essential \
        dsniff \
        iproute2 \
        iptables \
        iputils-ping \
        libnetfilter-queue-dev \
        net-tools \
        tcpdump

# Install Python dependencies
RUN --mount=type=bind,source=mitm-requirements.txt,target=/tmp/requirements.txt \
    --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    pip3 install --root-user-action=ignore --break-system-packages -U pip && \
    pip3 install --root-user-action=ignore --break-system-packages -r /tmp/requirements.txt

# Sleep to not have the container exit immediately
CMD ["sleep", "10d"]


FROM docker.io/alpine:3.20 AS client

# Install required packages
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk update && \
    apk add --update \
        iptables \
        nano \
        nmap \
        nmap-nselibs \
        nmap-scripts

# Copy in required scripts
COPY nmap-scripts /usr/share/nmap/scripts
COPY --chmod=0755 client.sh /client.sh

CMD ["/client.sh"]
