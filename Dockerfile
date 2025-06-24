FROM python:3.11-bullseye

ARG VERSION=dev
ENV VERSION=$VERSION

COPY . /app
WORKDIR /app

ENV CACHE_DEFAULT_TIMEOUT="3600"
ENV CACHE_TYPE="simple"
ENV CACHE_REDIS_HOST="redis"
ENV CACHE_REDIS_DB=4
ENV FLASK_APP="app.py"

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "8", "app:app"]
