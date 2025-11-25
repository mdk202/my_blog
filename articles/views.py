from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from articles.forms import CommentsForm
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


class ArticleView(FormMixin, ReactionMixin, DetailView):
    template_name = 'articles/news.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'
    form_class = CommentsForm

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['username'] = self.request.user.username
            initial['email'] = self.request.user.email
        return initial

    def get_object(self, queryset=None):
        news = Article.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return self.get_mixin_context(context)


class AddCommentView(LoginRequiredMixin, ArticleView):
    def get_success_url(self, **kwargs):
        return reverse_lazy('catalog:article', kwargs={'article_slug':
                                                       self.get_object().slug})

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.article = self.get_object()
        if form.data['comment_parent']:
            self.object.parent_id = int(form.data['comment_parent'])
        self.object.save()
        messages.success(self.request, f'{self.request.user.username},\
                                         Ваш комментарий успешно добавлен!')
        return super().form_valid(form)


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