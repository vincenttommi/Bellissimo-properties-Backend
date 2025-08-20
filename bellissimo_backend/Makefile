SHELL := /bin/bash

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | \
	awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
	sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

install:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

run:
	venv/bin/python manage.py runserver

migration:
	venv/bin/python manage.py makemigrations

migrate:
	venv/bin/python manage.py migrate

superuser:
	venv/bin/python manage.py createsuperuser

heroku:
	git push heroku master

deploy:
	docker-compose build
	docker-compose up -d

down:
	docker-compose down
