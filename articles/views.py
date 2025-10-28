from django.shortcuts import render


def catalog(request, category_slug=None):
    context ={
        'title': 'Каталог',
    }
    return render(request, 'articles/catalog.html', context)
