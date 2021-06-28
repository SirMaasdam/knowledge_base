import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from articles.forms import SearchForm
from articles.models import Article
from articles.article_services import get_article_by_search, get_articles, get_paginator_page, create_article
from cms.cms_decorators import ajax_required
from cms.create_content_services import manage_text_content, manage_image_content
from articles.article_services import update_time_edit


@login_required
def article_manage_list_view(request):
    """Returns list of user's articles that he owner"""
    form = SearchForm()
    if 'search' in request.GET:
        articles = get_article_by_search(request_search=request.GET,
                                         user=request.user.id,
                                         manager='objects')
    else:
        articles = get_articles(user=request.user.id,
                                manager='objects')
    page = request.GET.get('page')
    articles = get_paginator_page(articles=articles,
                                  page=page)
    return render(request,
                  'manage/list.html',
                  {'articles': articles,
                   'page': page,
                   'form': form})


@login_required
def articles_create_view(request):
    """Creates new Article"""
    article = create_article(request.user)
    return redirect(article.get_absolute_url_for_manage())


# @if_owner
@login_required
def article_manage_detail_view(request, slug):
    """Details of Article to edit"""
    article = get_object_or_404(Article,
                                slug=slug,
                                user=request.user)
    return render(request,
                  'manage/detail.html',
                  {'article': article})


@ajax_required
@login_required
def create_update_delete_content_view(request):
    """Create, update ,delete Articles Content with text content"""
    request_data = json.loads(request.body.decode('utf-8'))
    article = manage_text_content(request_data=request_data,
                                  user=request.user,
                                  article=None)
    if article:
        update_time_edit(article=article)
    return JsonResponse({'status': 'OK'})


@ajax_required
@login_required
def create_update_delete_content_with_file_view(request):
    """Create, update ,delete Articles Content with file content"""
    article = manage_image_content(request_data=dict(request.POST),
                                   user=request.user,
                                   files=request.FILES,
                                   article=None)
    if article:
        update_time_edit(article=article)
    return JsonResponse({'status': 'OK'})

