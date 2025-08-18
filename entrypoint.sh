#!/bin/sh
set -e


#Run database migrations automatically(optional but common)
python manage.py migrate --noinput


if ["$DJANGO_ENV"= "development" ]; then
    echo "starting Django development server..."
    python manage.py  runserver 0.0.0.0:8000
else:
    echo  "Starting Gunicorn serve...r
    gunicorn -bind 0.0.0.0:8--
