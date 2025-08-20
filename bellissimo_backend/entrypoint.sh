#!/bin/sh
set -e

echo "🏗️  Starting entrypoint..."

# Wait for the database to be ready
if [ "$DATABASE_HOST" != "" ]; then
  echo "⏳ Waiting for Postgres at $DATABASE_HOST:$DATABASE_PORT..."
  until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" > /dev/null 2>&1; do
    sleep 1
  done
  echo "✅ Postgres is ready!"
fi

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Collect static files (optional, but common in prod)
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Finally start Django server (adjust if you use gunicorn/uvicorn)
echo "🚀 Starting Django..."
exec python manage.py runserver 0.0.0.0:8000
