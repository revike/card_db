from django.contrib.auth.models import User
from django.core.management import BaseCommand

from card.settings import ADMIN_LOGIN, ADMIN_PASSWORD, ADMIN_EMAIL


class Command(BaseCommand):
    """Команда для создания супер юзера"""

    def handle(self, *args, **options):
        if not User.objects.filter(username=ADMIN_LOGIN, is_staff=True,
                                   is_superuser=True, is_active=True):
            User.objects.create_superuser(
                username=ADMIN_LOGIN, password=ADMIN_PASSWORD, is_active=True,
                email=ADMIN_EMAIL)
