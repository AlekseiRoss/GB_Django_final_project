from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import os


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
        words_number = 8
        max_len = 32
        if len(str(self.cooking_steps)) > max_len:
            return str(self.cooking_steps)[:max_len]+'...'
        words = str(self.cooking_steps).split()
        trimmed_text = ' '.join(words[:words_number])
        trimmed_text = trimmed_text.replace('\\n', '\n')
        if len(words) > words_number:
            trimmed_text += '...'
        return trimmed_text

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'recipe_id': self.pk})

    def __str__(self):
        return self.title
