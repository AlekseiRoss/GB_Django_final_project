from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Recipe, Category
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create a new recipe'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str,
                            help='Title of the recipe')
        parser.add_argument('description', type=str,
                            help='Description of the recipe')
        parser.add_argument('cooking_steps', type=str,
                            help='Steps for cooking the recipe')
        parser.add_argument('preparation_time', type=int,
                            help='Preparation time in minutes')
        parser.add_argument('image_path', type=str,
                            help='Path to the image of the recipe')
        parser.add_argument('author_username', type=str,
                            help='Username of the recipe author')
        parser.add_argument('category_name', type=str,
                            help='Name of the category for the recipe')

    def handle(self, *args, **kwargs):
        title = kwargs['title']
        description = kwargs['description']
        cooking_steps = kwargs['cooking_steps']
        preparation_time = timezone.timedelta(
            minutes=kwargs['preparation_time'])
        image_path = kwargs['image_path']
        author_username = kwargs['author_username']
        category_name = kwargs['category_name']

        # Проверяем существует ли пользователь с указанным именем автора
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"User with username '{author_username}' does not exist."))
            return

        # Проверяем существует ли категория с указанным названием
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"Category with name '{category_name}' does not exist."))
            return

        # Создаем и сохраняем новый объект Recipe
        recipe = Recipe.objects.create(
            title=title,
            description=description,
            cooking_steps=cooking_steps,
            preparation_time=preparation_time,
            image=image_path,
            author=author,
            category=category
        )
        self.stdout.write(self.style.SUCCESS(
            f"Recipe '{title}' created successfully."))
