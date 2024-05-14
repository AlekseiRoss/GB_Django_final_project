from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


class Home(DataMixin, ListView):
    model = Recipe
    template_name = 'myapp/index.html'
    context_object_name = 'recipes'

    # Функция передаёт в шаблон стат и динам данные
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for recipe in context['recipes']:
            recipe.cooking_steps = recipe.get_summary()
        c_def = self.get_user_context(title='Главная страница',
                                      cat_selected=0)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Recipe.objects.filter(is_published=True)\
            .order_by('-time_update')


class ShowCategory(DataMixin, ListView):
    model = Recipe
    template_name = 'myapp/index.html'
    context_object_name = 'recipes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for recipe in context['recipes']:
            recipe.cooking_steps = recipe.get_summary()
        cat_id = self.kwargs['cat_id']
        category = get_object_or_404(Category, pk=cat_id)
        c_def = self.get_user_context(title=category.name, cat_selected=cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        return Recipe.objects.filter(is_published=True, category__pk=cat_id)\
            .order_by('-time_update')


class ShowRecipe(DataMixin, DetailView):
    model = Recipe
    template_name = 'myapp/recipe.html'
    context_object_name = 'recipe'
    pk_url_kwarg = 'recipe_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'].cooking_steps = self.object.formatted_cooking_steps
        c_def = self.get_user_context(title=self.object.title,
                                      cat_selected=self.object.category.pk)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class AddRecipe(LoginRequiredMixin, DataMixin, CreateView):
    template_name = 'myapp/add_recipe.html'
    form_class = AddRecipeForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить рецепт')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        try:
            form.save(author_id=1)
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


class RegisterView(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'myapp/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class Custom404View(View):
    def get(self, request, exception):
        return render(request, 'myapp/404.html', status=404)
