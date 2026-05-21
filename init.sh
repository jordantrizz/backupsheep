#!/bin/bash

set -e

APP_PROCESS=${APP_PROCESS:-web}
RUN_MIGRATIONS=${RUN_MIGRATIONS:-true}

if [ "$RUN_MIGRATIONS" = "true" ]; then
	python manage.py migrate
fi

if [ "${APP_CACHE_BACKEND:-}" = "database" ] && [ "$APP_PROCESS" = "web" ]; then
	python manage.py createcachetable core_cache >/dev/null 2>&1 || true
fi

case "$APP_PROCESS" in
	web)
		service nginx start
		python manage.py collectstatic --noinput
		exec gunicorn backupsheep.wsgi:application --workers=4 --timeout=3600 --bind 0.0.0.0:8000
		;;
	worker)
		exec celery -A backupsheep worker --loglevel=INFO
		;;
	beat)
		exec celery -A backupsheep beat --loglevel=INFO
		;;
	*)
		exec "$@"
		;;
esac

