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
    image = models.ImageField(upload_to='recipes/images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @property
    def formatted_cooking_steps(self):
        if self.cooking_steps:
            return str(self.cooking_steps).replace('\\n', '\n')
        else:
            return ''

    def get_summary(self):
        # Разбиваем текст на слова
        words = str(self.cooking_steps).split()
        # Обрезаем текст после первых 8 слов
        trimmed_text = ' '.join(words[:8])
        # Заменяем символы '\n' на фактические переносы строк '\n'
        trimmed_text = trimmed_text.replace('\\n', '\n')
        # Добавляем многоточие в конце
        trimmed_text += '...'
        return trimmed_text

    def __str__(self):
        return self.title
