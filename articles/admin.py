from django.contrib import admin

from articles.models import Category


@admin.register(Category)
class PersonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
