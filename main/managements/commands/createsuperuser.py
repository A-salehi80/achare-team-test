from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import CommandError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser, with phone number as a required field.'

    def handle(self, *args, **kwargs):
        Phone = input('Phone number: ')
        username = input('Username: ')
        password = input('Password: ')

        if User.objects.filter(Phone=Phone).exists():
            raise CommandError('Phone number is already taken')

        user = User.objects.create_superuser(Phone=Phone, username=username, password=password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))