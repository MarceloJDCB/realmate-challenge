.PHONY: init up down migrate makemigrations poetry_lock

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

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations