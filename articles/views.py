from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView, ListView

from articles.mixins import ReactionMixin
from articles.models import Article, Like
from articles.utils import q_search


class CatalogView(ReactionMixin, ListView):
    model = Article
    template_name = 'articles/catalog.html'
    context_object_name = 'articles'
    paginate_by = 4

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        sort = self.request.GET.get('sort')
        query = self.request.GET.get('q')

        if category_slug == 'all':
            articles = super().get_queryset()
        elif query:
            articles = q_search(query)
        else:
            articles = super().get_queryset().\
                               filter(category__slug=category_slug)

        if sort:
            articles = articles.order_by(sort)

        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['slug_url'] = self.kwargs.get('category_slug')
        return self.get_mixin_context(context)


class ArticleView(ReactionMixin, DetailView):
    template_name = 'articles/news.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        news = Article.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return self.get_mixin_context(context)


class AddLikeView(ReactionMixin, View):
    def post(self, request, **kwargs):
        article_id = request.POST.get('article_id')
        article = Article.objects.get(pk=article_id)
        like = self.get_like(request, article)

        if not like.exists():
            Like.objects.create_like(request, article)
            message = 'Лайк добавлен'
        else:
            like.delete()
            message = 'Лайк убран'

        like_items_html = render_to_string(
            "articles/includes/included_reactions.html",
            {"article": article},
            request=request
        )

        response_data = {
            "message": message,
            "like_items_html": like_items_html,
        }
        return JsonResponse(response_data)