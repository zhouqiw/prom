#!/bin/sh


python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations alert
python manage.py migrate alert
python manage.py runserver ${1}
echo "$@"