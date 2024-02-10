# loading and exporting all env vars from .env file automatically
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

APP_NAME="python-boilerplate-project"
IMAGE_NAME="python-boilerplate-project"
VERSION="latest"

################################
# COMMANDS TO RUN LOCALLY
################################

local/install: generate-default-env-file
	poetry install

local/tests:
	poetry run pytest -s --cov-report=html --cov-report=term --cov . 

local/lint:
	poetry run ruff check .
	
local/lint/fix:
	poetry run ruff . --fix --exit-non-zero-on-fix

local/run:
	poetry run python src/main.py

############################################
# COMMANDS TO RUN USING DOCKER (RECOMMENDED)
############################################

docker/install: generate-default-env-file
	docker-compose build ${APP_NAME}

docker/up:
	docker-compose up -d

docker/down:
	docker-compose down --remove-orphans

docker/test:
	docker-compose run ${APP_NAME} poetry run pytest --cov-report=html --cov-report=term --cov .

docker/lint:
	docker-compose run ${APP_NAME} poetry run ruff check .

docker/lint/fix:
	docker-compose run ${APP_NAME} poetry run ruff . --fix --exit-non-zero-on-fix

docker/run:
	docker-compose run ${APP_NAME} poetry run python src/main.py

####################################
# DOCKER IMAGE COMMANDS
####################################

docker/image/build:
	docker build . --target production -t ${IMAGE_NAME}:${VERSION}

docker/image/push:
	docker push ${IMAGE_NAME}:${VERSION}

##################
# HEPFUL COMMANDS
##################

generate-default-env-file:
	@if [ ! -f .env ]; then cp env.template .env; fi;
