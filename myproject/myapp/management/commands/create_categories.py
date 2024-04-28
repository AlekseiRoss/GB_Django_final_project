from django.core.management.base import BaseCommand
from myapp.models import Category


class Command(BaseCommand):
    help = 'Populate Category model with predefined categories'

    def handle(self, *args, **kwargs):
        categories = ['Завтраки', 'Первые блюда', 'Вторые блюда', 'Салаты',
                      'Десерты', 'Напитки']

        for category in categories:
            Category.objects.create(name=category)

        self.stdout.write(
            self.style.SUCCESS('Categories have been successfully populated.'))
