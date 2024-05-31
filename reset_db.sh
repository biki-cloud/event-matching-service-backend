#!/bin/sh

echo "DJANGO_SUPERUSER_EMAIL: $DJANGO_SUPERUSER_EMAIL"
echo "DJANGO_SUPERUSER_PASSWORD: $DJANGO_SUPERUSER_PASSWORD"
echo "HOST_NAME: $HOST_NAME"

rm db.sqlite3

# Create new migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=$(printenv DJANGO_SUPERUSER_EMAIL)
export DJANGO_SUPERUSER_PASSWORD=$(printenv DJANGO_SUPERUSER_PASSWORD)
python manage.py createsuperuser --noinput --name admin --email $DJANGO_SUPERUSER_EMAIL

# Load initial data
# python manage.py loaddata fixtures/init_data.json
