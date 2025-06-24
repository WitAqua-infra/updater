FROM python:3.11-bullseye

ARG VERSION=dev
ENV VERSION=$VERSION

COPY . /app
WORKDIR /app

ENV GERRIT_URL="https://gerrit.witaqua.org/"
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

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "8", "app:app"]
