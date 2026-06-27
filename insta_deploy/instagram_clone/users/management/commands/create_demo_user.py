"""
Management command: create_demo_user

Automatically creates a demo account so markers can log in immediately
after deployment without any manual setup.

Run automatically in Procfile on every deploy:
    python manage.py create_demo_user
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

DEMO_USERNAME = 'demo'
DEMO_EMAIL    = 'demo@instaclone.app'
DEMO_PASSWORD = 'Demo@1234'


class Command(BaseCommand):
    help = 'Creates the demo test user if it does not already exist.'

    def handle(self, *args, **options):
        if User.objects.filter(username=DEMO_USERNAME).exists():
            self.stdout.write(
                self.style.WARNING(f'Demo user "{DEMO_USERNAME}" already exists — skipping.')
            )
            return

        User.objects.create_superuser(
            username=DEMO_USERNAME,
            email=DEMO_EMAIL,
            password=DEMO_PASSWORD,
            bio='Demo account for testing. 📸',
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Demo user created.\n'
                f'  Username : {DEMO_USERNAME}\n'
                f'  Password : {DEMO_PASSWORD}\n'
                f'  Admin    : /admin/'
            )
        )
