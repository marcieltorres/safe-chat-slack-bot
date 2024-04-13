FROM python:3.11.0-slim-buster AS base

WORKDIR /src

# Installing gettext
RUN apt-get update -y && apt-get install gettext -y

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

# Generating po file with translations
RUN msgfmt -o src/locales/en/LC_MESSAGES/base.mo src/locales/en/LC_MESSAGES/base.po
RUN msgfmt -o src/locales/pt_BR/LC_MESSAGES/base.mo src/locales/pt_BR/LC_MESSAGES/base.po

# Starting the Bot
CMD poetry run python src/bot.py
