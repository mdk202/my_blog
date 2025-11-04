from django import template
from django.utils.http import urlencode

from articles.models import Category


register = template.Library()


@register.simple_tag()
def tag_categories():
    """Получение всех категорий"""
    return Category.objects.all()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    """Настройка пагинации для фильтрации и поиска"""
    # Получаем параметры GET запроса из request (фильтры, поиск)
    query = context['request'].GET.dict()
    # Добавляем параметр page
    query.update(kwargs)
    return urlencode(query)