FROM nginx:1.27-alpine AS server

# Install required packages
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk update && \
    apk add --update \
        openssl

# Add config and website
RUN rm -f /etc/nginx/conf.d/*
COPY ./server/default.conf /etc/nginx/conf.d/default.conf
COPY ./server/index.html /www/index.html

# PART B
#RUN mkdir /certs
#RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /certs/selfsigned.key -out /certs/selfsigned.crt -subj "/C=CH/ST=Vaud/L=Lausanne/O=server/OU=server/CN=server"

# PART C (Files provided to skip the .csr process)
#COPY --chmod=0640 ./server/request.key /certs/request.key
#COPY --chmod=0640 ./server/request.crt /certs/request.crt

FROM python:3.12-alpine AS verifier

# Install required packages
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk update && \
    apk add --update \
        openssl

# Install Python dependencies
RUN --mount=type=bind,source=./verifier/requirements.txt,target=/tmp/requirements.txt \
    --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    pip3 install --root-user-action=ignore --break-system-packages -U pip && \
    pip3 install --root-user-action=ignore --break-system-packages -r /tmp/requirements.txt

COPY --chmod=0644 ./verifier/verifier.py /app/verifier.py
COPY --chmod=0640 ./verifier/rootCA.key  /app/rootCA.key
COPY --chmod=0640 ./verifier/rootCA.pem  /app/rootCA.pem
COPY --chmod=0755 ./verifier/script.sh   /app/script.sh

CMD ["/app/script.sh"]
