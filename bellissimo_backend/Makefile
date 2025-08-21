# Makefile for Bellissimo Properties Backend

PROJECT_NAME=bellissimo_backend
COMPOSE=docker compose -p $(PROJECT_NAME)

# --- Development ---
dev:
	$(COMPOSE) up --build

dev-down:
	$(COMPOSE) down -v

dev-logs:
	$(COMPOSE) logs -f

dev-shell:
	$(COMPOSE) exec django-web bash

# --- Production ---
prod:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up --build -d

prod-down:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml down -v

prod-logs:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml logs -f

prod-shell:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml exec django-web bash

# --- Utilities ---
migrate:
	$(COMPOSE) exec django-web python manage.py migrate

makemigrations:
	$(COMPOSE) exec django-web python manage.py makemigrations

createsuperuser:
	$(COMPOSE) exec django-web python manage.py createsuperuser

collectstatic:
	$(COMPOSE) exec django-web python manage.py collectstatic --noinput
