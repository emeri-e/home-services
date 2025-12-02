#!/usr/bin/env bash
set -euo pipefail

# Wait for Postgres if configured
if [ -n "${DATABASE_HOST:-}" ]; then
  DB_HOST="${DATABASE_HOST}"
  DB_PORT="${DATABASE_PORT:-5432}"
  echo "Waiting for Postgres at ${DB_HOST}:${DB_PORT}..."
  # wait until the port is open
  until nc -z "${DB_HOST}" "${DB_PORT}"; do
    sleep 1
  done
  echo "Postgres is up."
fi

# Apply migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the app
if [ -n "${GUNICORN_MODULE:-}" ]; then
  # Start gunicorn with sensible defaults; workers can be tuned
  echo "Starting Gunicorn ($GUNICORN_MODULE) on 0.0.0.0:8000"
  exec gunicorn --bind 0.0.0.0:8000 --workers 3 "$GUNICORN_MODULE"
else
  echo "GUNICORN_MODULE not set — starting Django development server"
  exec python manage.py runserver 0.0.0.0:8000
fi