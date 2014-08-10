web: gunicorn mailinglist.wsgi --log-file -
worker: celery -A mailinglist worker -l info
