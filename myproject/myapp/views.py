from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить рецепт", 'url_name': 'add_recipe'},
        {'title': "Войти", 'url_name': 'login'}]


class Home(ListView):
    model = Recipe
    template_name = 'myapp/index.html'
    context_object_name = 'recipes'

    # Функция передаёт в шаблон и стат и динам данные
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        for recipe in context['recipes']:
            recipe.cooking_steps = recipe.get_summary()
        return context

    def get_queryset(self):
        return Recipe.objects.filter(is_published=True)


class ShowCategory(ListView):
    model = Recipe
    template_name = 'myapp/index.html'
    context_object_name = 'recipes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs['cat_id']
        category = get_object_or_404(Category, pk=cat_id)
        context['menu'] = menu
        context['title'] = category.name
        context['cat_selected'] = cat_id
        for recipe in context['recipes']:
            recipe.cooking_steps = recipe.get_summary()
        return context

    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        return Recipe.objects.filter(is_published=True,
                                     category__pk=cat_id)


class ShowRecipe(DetailView):
    model = Recipe
    template_name = 'myapp/recipe.html'
    context_object_name = 'recipe'
    pk_url_kwarg = 'recipe_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = self.object.title
        context['cat_selected'] = self.object.category.pk
        context['recipe'].cooking_steps = self.object.formatted_cooking_steps
        return context


class AddRecipe(CreateView):
    template_name = 'myapp/add_recipe.html'
    form_class = AddRecipeForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить рецепт'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        try:
            # Создаем временный путь для сохранения изображения
            current_time = timezone.now().strftime('%Y%m%d%H%M%S')
            image = form.cleaned_data.pop('image')
            fs = FileSystemStorage()
            # Сохраняем изображение
            filename = fs.save(f'recipes/images/{current_time}/{image.name}',
                               image)
            # Создаем объект Recipe
            form.instance.image = filename
            form.instance.author_id = 1
            form.instance.time_create = current_time
            form.instance.time_update = current_time
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, f'Ошибка добавления поста: {str(e)}')
            return super().form_invalid(form)


class AboutView(View):
    def get(self, request):
        return HttpResponse('О сайте')


class LoginView(View):
    def get(self, request):
        return HttpResponse('Вход')


class RegisterView(View):
    def get(self, request):
        return HttpResponse('Регистрация')


class Custom404View(View):
    def get(self, request, exception):
        return render(request, 'myapp/404.html', status=404)
