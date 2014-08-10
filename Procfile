web: gunicorn mailinglist.wsgi --log-file -
worker: python manage.py celeryd -B -l info
