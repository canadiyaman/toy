#!/bin/bash
# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Loading Initial data"
python python python manage.py loadtestdata

echo "Run server"
python manage.py runserver 0.0.0.0:8000