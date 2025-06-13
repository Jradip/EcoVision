#!/bin/sh

if [ ! -f "/app/db.sqlite3" ]; then
  echo "No database found, running makemigrations and migrate..."
  python manage.py makemigrations --noinput
  python manage.py migrate --noinput

  echo "Loading initial data..."
  python manage.py loaddata initial_waste_types.json
  python manage.py loaddata initial_waste_bank.json
  python manage.py loaddata initial_trash_can.json
else
  echo "Database already exists, skipping migration and data load."
fi

exec gunicorn eco_vision_api_django.wsgi:application --bind 0.0.0.0:8000 --workers 3
