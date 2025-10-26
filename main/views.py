from django.shortcuts import render


def index(request):
    context ={
        'title': 'Главная страница',
        'content': 'Контент на странице',
    }
    return render(request, 'main/index.html', context)

def about(request):
    context ={
        'title': 'О команде',
        'content': 'Контент на странице',
    }
    return render(request, 'main/index.html', context)
