web: gunicorn Trabazo.wsgi:application
worker: celery worker --app=taskapp --loglevel=info
python manage.py collectstatic --noinput
