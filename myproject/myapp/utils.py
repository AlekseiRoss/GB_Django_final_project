from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить рецепт", 'url_name': 'add_recipe'}]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('recipe'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = -1
        return context
