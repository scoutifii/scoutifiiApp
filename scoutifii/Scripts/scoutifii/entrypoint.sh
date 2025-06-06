#!/bin/bash
APP_PORT=${PORT:-5000}
cd /app/
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm scoutify.wsgi:application --bind "0.0.0.0:${APP_PORT}"