#!/bin/sh
set -e

# Run database migrations automatically (optional but common)
python manage.py migrate --noinput

if [ "$DJANGO_ENV" = "development" ]; then
    echo "Starting Django development server..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn server..."
    gunicorn --bind 0.0.0.0:8000 --workers 3 bellissimo_backend.wsgi:application
fi
