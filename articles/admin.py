from django.contrib import admin

from articles.models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}