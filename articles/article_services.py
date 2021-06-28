import redis
from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from django.http import QueryDict
from django.contrib.auth import get_user_model
from django.utils import timezone
from .forms import SearchForm
from .models import Article

User = get_user_model()

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def get_paginator_page(articles: QuerySet, page: int):
    """Returns page with articles by its number"""
    paginator = Paginator(articles, 3)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return articles


def get_articles(user: int = None, manager: str = 'published') -> QuerySet:
    """Returns Article with different managers"""
    manager = getattr(Article, manager)
    return manager.filter(user=user) if user else manager.all()


def get_search_result(search: str, user: int, manager: str = 'published') -> QuerySet:
    """Searches for articles that meet the search query using a trigram similarity search"""
    manager = getattr(Article, manager)
    if user:
        articles = manager.annotate(
            similarity=TrigramSimilarity('title', search),
        ).filter(similarity__gt=0.1, user=user).order_by('-similarity')
    else:
        articles = manager.annotate(
            similarity=TrigramSimilarity('title', search),
        ).filter(similarity__gt=0.1).order_by('-similarity')
    return articles


def add_or_show_total_views(article_id: int, add: bool = False):
    """Using Redis, it adds and returns count of views"""
    if add:
        return r.incr(f'image:{article_id}:views')
    else:
        return int(r.get(f'image:{article_id}:views'))


def get_article_by_search(request_search: QueryDict, user: int = None, manager: str = 'published') -> QuerySet:
    """Return Articles by search"""
    form = SearchForm(request_search)
    if form.is_valid():
        search = form.cleaned_data['search']
        return get_search_result(search=search,
                                 user=user,
                                 manager=manager)


def update_time_edit(article: Article) -> None:
    """Updates time edit or Article status"""
    article.updated = timezone.now()
    if article.draft:
        article.draft = False
    article.save()


def create_article(user: User):
    """Creates new Article"""
    article = Article.objects.create(user=user,
                                     title="Введите название статьи",
                                     draft=True)
    return article
