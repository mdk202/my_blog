from django.urls import path
from articles import views

app_name='articles'

urlpatterns = [
    path('<slug:category_slug>/', views.catalog, name='index'),
    path('news/<slug:article_slug>/', views.article, name='article'),
]