from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a new Django user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str,
                            help='Username for the new user')
        parser.add_argument('email', type=str,
                            help='Email for the new user')
        parser.add_argument('password', type=str,
                            help='Password for the new user')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        # Создаем нового пользователя
        user = User.objects.create_user(username, email, password)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created user "{username}"'))
