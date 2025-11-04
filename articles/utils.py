from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from articles.models import Article


def q_search(query):
    """Полнотекстовый поиск по статьям"""
    vector = SearchVector("title", "summary", "description")
    query = SearchQuery(query)
    return Article.objects.alias(rank=SearchRank(vector, query)).\
                           filter(rank__gt=0).\
                           order_by("-rank", "-date_creation")
