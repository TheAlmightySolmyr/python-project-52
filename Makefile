.PHONY: install build migrate collectstatic dev render-start

install:
	uv sync

build:
	./build.sh

check:
	uv run ruff check

fix:
	uv run ruff check --fix

render-start:
	gunicorn task_manager.wsgi

dev:
	uv run manage.py runserver

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput