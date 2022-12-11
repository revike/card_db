#!/bin/sh

# shellcheck disable=SC2164
cd card

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py create_admin
sleep 5
python3 manage.py search_index --rebuild -f
python3 manage.py runserver 0.0.0.0:8000
