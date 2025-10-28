from django.urls import path
from articles import views

app_name='articles'

urlpatterns = [
    path('<slug:category_slug>/', views.catalog, name='index'),
]