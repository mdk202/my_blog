from django.urls import path
from articles import views

app_name='articles'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('news/<slug:article_slug>/', views.ArticleView.as_view(), name='article'),
    path('news/<slug:article_slug>/like/', views.AddLikeView.as_view(), name='liked'),

]