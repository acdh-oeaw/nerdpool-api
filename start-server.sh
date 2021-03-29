#!/usr/bin/env bash
# start-server.sh
cd nerdpool && python manage.py collectstatic --no-input && python manage.py migrate
if [ -n "$IMPORTDATA" ]; then
    (python manage.py import_RITA && python manage.py import_RTA && python manage.py import_MRP)
fi
gunicorn nerdpool.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 & nginx -g "daemon off;"
