from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cooking_steps = models.TextField()
    preparation_time = models.DurationField()
    image = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    @property
    def formatted_cooking_steps(self):
        if self.cooking_steps:
            return str(self.cooking_steps).replace('\\n', '\n')
        else:
            return ''

    def get_summary(self):
        max_length = 40  # Максимальная длина текста
        cooking_steps_str = str(self.cooking_steps)
        # Обрезаем текст до максимальной длины
        trimmed_text = cooking_steps_str[:max_length]
        # Если текст был обрезан, ищем последнее пробельное место для
        # корректного обрезания слов
        if len(trimmed_text) < len(cooking_steps_str):
            last_space_index = trimmed_text.rfind(' ')
            if last_space_index != -1:
                trimmed_text = trimmed_text[:last_space_index]
        # Заменяем символы '\\n' на переносы строк
        trimmed_text = trimmed_text.replace('\\n', '\n')
        # Если текст был обрезан, добавляем многоточие в конце
        if len(trimmed_text) < len(cooking_steps_str):
            trimmed_text += '...'
        return trimmed_text

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'recipe_id': self.pk})

    def __str__(self):
        return self.title
