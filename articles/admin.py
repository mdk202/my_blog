from django.contrib import admin

from articles.models import Category, Article, Like, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Like)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_timestamp')


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'text_comment', 'parent', 'created_timestamp')
