from django import template
from ..models import Category

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(id_filter=None):
    if not id_filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=id_filter)


@register.inclusion_tag('myapp/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}
