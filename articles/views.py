from django.shortcuts import render

from articles.models import Article


def catalog(request, category_slug=None):
    articles = Article.objects.all()
    context ={
        'title': 'Каталог',
        'articles': articles,
    }
    return render(request, 'articles/catalog.html', context)

def article(request, article_slug):
    article = Article.objects.get(slug=article_slug)
    context ={
        'title': 'Новость',
        'article': article,
    }
    return render(request, 'articles/news.html', context)