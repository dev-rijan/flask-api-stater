FROM python:3.8.3-slim-buster as app
LABEL maintainer="Rijan adhikari <rijanadhikari@gmail.com>"

WORKDIR /app

COPY Pipfile Pipfile

ENV BUILD_DEPS="build-essential" \
    APP_DEPS="curl libpq-dev"

RUN apt-get update \
  && apt-get install -y ${BUILD_DEPS} ${APP_DEPS} --no-install-recommends \
  && pip3 install pipenv \
  && pipenv install \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /usr/share/doc && rm -rf /usr/share/man \
  && apt-get purge -y --auto-remove ${BUILD_DEPS} \
  && apt-get clean

ARG FLASK_ENV="production"
ENV FLASK_ENV="${FLASK_ENV}" \
    FLASK_APP="src.app" \
    PYTHONUNBUFFERED="true"

COPY . .

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]

EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "-c", "python:config.gunicorn", "src.app:create_app()"]
