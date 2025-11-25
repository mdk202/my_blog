from django import template
from django.utils.http import urlencode

from articles.models import Category, Comment


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


@register.simple_tag
def tag_comments(article):
    """Получение всех комментариев на статье"""
    # Получаем все коммент. для статьи, отсортированные по дате
    all_comments = Comment.objects.filter(article=article)\
                                  .select_related('user', 'parent')\
                                  .order_by('created_timestamp')
    # Создаем словарь для доступа к коммент. по pk
    comment_map = {comment.pk: comment for comment in all_comments}
    # Список родительских коммент.
    root_comments = []
    for comment in all_comments:
        # Добавляем каждому коммент. поле (список) для хранения дочер. коммент.
        comment.nested_children = []
        # Если у коммент. нет родителя добавляем его в root_comments, иначе
        # заносим коммент. в поле nested_children соответствующего родителя
        if comment.parent is None:
            root_comments.append(comment)
        else:
            parent = comment_map.get(comment.parent_id)
            if parent:
                parent.nested_children.append(comment)
    return root_comments