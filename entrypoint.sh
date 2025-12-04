#!/bin/sh

if [ "$DATABASE" = "staging" ]
then
    echo "Waiting for postgres..."

    while ! nc -x $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
# pytest -vvv
python manage.py runserver 0.0.0.0:8000

exec "$@"