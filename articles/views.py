from django.shortcuts import render, get_object_or_404
from comments.comment_services import create_comment
from comments.forms import CommentForm
from .models import Article
from .forms import SearchForm
from .article_services import get_articles, get_article_by_search, get_paginator_page, add_or_show_total_views


def article_list_view(request):
    """Returns list articles"""
    form = SearchForm()
    if 'search' in request.GET:
        articles = get_article_by_search(request_search=request.GET)
    else:
        articles = get_articles()
    page = request.GET.get('page')
    articles = get_paginator_page(articles=articles, page=page)
    return render(request,
                  'articles/list.html',
                  {'articles': articles,
                   'page': page,
                   'form': form})


def article_detail_view(request, year, month, day, slug):
    """Details of Article"""
    comment_form = CommentForm()
    article = get_object_or_404(Article,
                                slug=slug,
                                created__year=year,
                                created__month=month,
                                created__day=day)
    if request.method == 'GET':
        total_views = add_or_show_total_views(add=True,
                                              article_id=article.id)
    if request.method == 'POST':
        total_views = add_or_show_total_views(article_id=article.id)
        create_comment(request_data=request.POST,
                       user=request.user,
                       article=article)
    return render(request,
                  'articles/detail.html',
                  {'article': article,
                   'comment_form': comment_form,
                   'total_views': total_views})
