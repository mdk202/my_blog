from django.views.generic import DetailView, ListView

from articles.models import Article
from articles.utils import q_search


class CatalogView(ListView):
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
        return context


class ArticleView(DetailView):
    template_name = 'articles/news.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        news = Article.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context
