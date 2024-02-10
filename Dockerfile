FROM python:3.11.0-slim-buster AS base

WORKDIR /src

COPY pyproject.toml .
RUN pip install poetry

FROM base AS dependencies
RUN poetry install --no-dev

FROM base AS development
RUN poetry install
COPY . .

FROM dependencies AS production
COPY src src
COPY settings.conf src
COPY logging.conf src
