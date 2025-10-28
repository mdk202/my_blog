from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=128, unique=True)
    slug = models.SlugField(verbose_name='URL',
                            max_length=128, blank=True, null=True)
    
    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name