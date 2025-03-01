.PHONY: init up down migrate makemigrations poetry_lock lint

_cp_env:
	cp .env.example .env

poetry_lock:
	poetry lock --no-update

init: _cp_env poetry_lock
	docker-compose build
	docker-compose up -d
	make migrate

up:
	docker-compose up -d

down:
	docker-compose down

rebuild:
	docker-compose down
	docker-compose up -d --build

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

restart:
	docker-compose restart

stop:
	docker-compose stop

raw_init:
	docker-compose build
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py createsuperuser

# Project specific cleaning
project-clean:
	docker-compose down -v
	docker volume ls -q -f "name=realmate-challenge" | xargs -r docker volume rm
	docker images -q "realmate-challenge*" | xargs -r docker rmi
	docker network ls -q -f "name=realmate-challenge" | xargs -r docker network rm
	docker container ls -a -q -f "name=realmate-challenge" | xargs -r docker rm

install:
	docker-compose exec web poetry install
	docker-compose exec celery poetry install

drop_db:
	docker compose down -v postgres

test:
	docker-compose exec web pytest

lint:
	docker-compose exec web flake8 .
