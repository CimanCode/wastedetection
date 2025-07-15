#!/bin/bash

echo "Apply database migrations"
python manage.py migrate

echo "Seed initial data"
python manage.py seed_trashinfo || echo "Skip seeding"

echo "Collect static files"
python manage.py collectstatic --noinput || echo "Skip collectstatic"

exec "$@"