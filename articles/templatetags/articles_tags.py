from django import template

from articles.models import Category


register = template.Library()


@register.simple_tag()
def tag_categories():
    return Category.objects.all()