from django.db.models import Case, When, Value

from articles.models import Article, Like


class ReactionMixin:
    def get_mixin_context(self, context):
        # Получаем информацию о кол-ве реакций на каждой статье
        # (либо для каталога, либо для конкретной статьи)
        if 'article' in context:
            articles = Article.objects.filter(pk=context['article'].pk)
            reactions_on_articles = Article.objects.counts_reactions(articles)
        else:
            articles = context['articles']
            # Условное выражение для сохранения порядка статей
            preserved_order = Case(*[When(id=id, then=Value(index)) for index, id in
                                   enumerate(articles.values_list('pk', flat=True))])
            reactions_on_articles = Article.objects.counts_reactions(articles)\
                                                   .order_by(preserved_order)

        # Получаем все статьи, которые лайкал конкретный пользователь
        articles_liked_user = Like.objects.liked_articles(self.request, articles)
        
        context['articles_liked_user'] = articles_liked_user
        if 'article' in context:
            context['article'] = reactions_on_articles.first()
        else:
            context['articles'] = reactions_on_articles
        return context


    def get_like(self, request, article):
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}
        query_kwargs['article'] = article
        return Like.objects.filter(**query_kwargs).select_related('article', 'user')
