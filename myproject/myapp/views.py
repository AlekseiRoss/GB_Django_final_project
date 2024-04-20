from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить рецепт", 'url_name': 'add_receip'},
        {'title': "Войти", 'url_name': 'login'}]


class HomeView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        for recipe in recipes:
            recipe.cooking_steps = recipe.get_summary()

        context = {
            'title': 'Главная страница',
            'recipes': recipes,
            'menu': menu,
            'selected_category': 0,
        }

        return render(request, 'myapp/index.html', context)


class ShowCategoryView(View):
    def get(self, request, cat_id):
        category = Category.objects.get(pk=cat_id)  # Получить объект категории
        title = category.name  # Извлечь имя категории
        recipes = Recipe.objects.filter(category_id=cat_id)
        for recipe in recipes:
            recipe.cooking_steps = recipe.get_summary()

        context = {
            'title': title,
            'recipes': recipes,
            'menu': menu,
            'selected_category': cat_id,
        }

        return render(request, 'myapp/index.html', context)


class RecipeView(View):
    def get(self, request, recipe_id):
        return HttpResponse(f"Отображение recipe с id = {recipe_id}")

class AboutView(View):
    def get(self, request):
        return HttpResponse('О сайте')


class AddReceipView(View):
    def get(self, request):
        return HttpResponse('Добавить рецепт')


class LoginView(View):
    def get(self, request):
        return HttpResponse('Вход')


class RegisterView(View):
    def get(self, request):
        return HttpResponse('Регистрация')


class Custom404View(View):
    def get(self, request, exception):
        return render(request, 'myapp/404.html', status=404)
