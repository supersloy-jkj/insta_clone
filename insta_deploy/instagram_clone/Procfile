release: python manage.py migrate --no-input && python manage.py create_demo_user
web: gunicorn instagram_clone.wsgi:application --bind 0.0.0.0:$PORT --log-file -
