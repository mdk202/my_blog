from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=128, unique=True)
    slug = models.SlugField(verbose_name='URL', max_length=128, unique=True,
                            blank=True, null=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:index', kwargs={"category_slug": self.slug})


class Article(models.Model):
    title = models.CharField(verbose_name='Название', max_length=128,
                             unique=True)
    slug = models.SlugField(verbose_name='URL', max_length=128, unique=True,
                            blank=True, null=True)
    summary = models.TextField(verbose_name='Описание', blank=True, null=True)
    description = models.TextField(verbose_name='Текст статьи', blank=True,
                                   null=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL,
                                 related_name='articles', null=True,
                                 verbose_name='Категория')
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='articles_images', blank=True, null=True)
    date_creation = models.DateTimeField(verbose_name='Дата создания',
                                         auto_now_add=True)
    date_update = models.DateTimeField(verbose_name='Дата обновления',
                                       auto_now=True)

    class Meta:
        db_table = 'article'
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
        ordering = ('-date_creation',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:article', kwargs={"article_slug": self.slug})