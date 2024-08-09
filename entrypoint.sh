#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run Django migrations
echo "Applying Django migrations..."
# python manage.py migrate

# Create a superuser with predefined credentials
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '', '123')
EOF

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput



# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8199 config.wsgi:application
