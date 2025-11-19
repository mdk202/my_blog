from django.contrib import admin

from articles.models import Category, Article, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Like)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_timestamp')