FROM golang:1.21-bullseye AS overmind
RUN GO111MODULE=on go install github.com/DarthSim/overmind/v2@latest

FROM python:3.11-slim-bullseye
COPY --from=overmind /go/bin/overmind /usr/local/bin/overmind

RUN apt-get update && apt-get install -y \
    tmux \
    && rm -rf /var/lib/apt/lists/*

ARG VERSION=dev
ENV VERSION=$VERSION

COPY . /app
WORKDIR /app

ENV GERRIT_URL="https://review.lineageos.org"
ENV CACHE_DEFAULT_TIMEOUT="3600"
ENV CACHE_TYPE="simple"
ENV CACHE_REDIS_HOST="redis"
ENV CACHE_REDIS_DB=4
ENV WIKI_INSTALL_URL="https://wiki.lineageos.org/devices/{device}/install"
ENV WIKI_INFO_URL="https://wiki.lineageos.org/devices/{device}"
ENV UPSTREAM_URL=""
ENV DOWNLOAD_BASE_URL="https://mirrorbits.lineageos.org"
ENV FLASK_APP="app.py"

RUN pip install -r requirements.txt

CMD ["/usr/local/bin/overmind", "start"]
