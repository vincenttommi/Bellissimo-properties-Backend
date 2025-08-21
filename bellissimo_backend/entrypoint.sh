#!/bin/bash
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

# Collect static files (optional, but kept for consistency)
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Print the local development URL
echo "🌐 Django application is running at http://localhost:8000"

# Finally start Django server
echo "🚀 Starting Django..."
exec python manage.py runserver 0.0.0.0:8000