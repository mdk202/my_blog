from django.db import models
from django.urls import reverse

from users.models import User


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


class ArticleManager(models.Manager):
    def counts_reactions(self, articles):
        """Возвращает QuerySet статей с аннотациями кол-ва реакций"""
        return self.filter(pk__in=articles).annotate(
            count_likes_on_article=models.Count('likes', distinct=True),
            count_comments_on_article=models.Count('comments', distinct=True))


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

    objects = ArticleManager()

    class Meta:
        db_table = 'article'
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
        ordering = ('-date_creation',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:article', kwargs={"article_slug": self.slug})


class LikeManager(models.Manager):
    def create_like(self, request, article):
        """Создание лайка на статье"""
        return self.create(user=request.user if request.user.is_authenticated else None,
                    session_key=request.session.session_key if not
                    request.user.is_authenticated else None,
                    article=article)
    
    def liked_articles(self, request, articles):
        """Возвращает ValuesQuerySet (pk) статей, которые лайкал пользователь"""
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        # Если пользователь не авторизован, создаем ему сессионный ключ
        elif not request.session.session_key:
            request.session.create()
            query_kwargs = {"session_key": request.session.session_key}
        else:
            query_kwargs = {"session_key": request.session.session_key}
        return self.filter(article__in=articles, **query_kwargs)\
                   .values_list('article', flat=True)


class Like(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE,
                                related_name='likes', verbose_name='Новость')
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                             related_name='likes', verbose_name='Пользователь',
                             blank=True, null=True)
    session_key = models.CharField(verbose_name='Сессионный ключ', max_length=32,
                                   blank=True, null=True)
    created_timestamp = models.DateTimeField(verbose_name='Дата добавления',
                                             auto_now_add=True)

    objects = LikeManager()

    class Meta:
        db_table = 'like'
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        if self.user:
            return f'{self.article} - {self.user}'
        return f'{self.article} - Аноним'


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                             related_name='comments', verbose_name='Автор',
                             blank=True, null=True)
    text_comment = models.TextField(verbose_name='Комментарий', max_length=500)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE,
                               related_name='children', blank=True, null=True,
                               verbose_name='Родительский комментарий')
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE,
                                related_name='comments', verbose_name='Статья')
    created_timestamp = models.DateTimeField(verbose_name='Дата добавления',
                                             auto_now_add=True)

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        if self.user:
            return f'{self.user} - {self.article}'
        return f'Неизвестный - {self.article}'