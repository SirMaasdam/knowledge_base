from django.http import QueryDict
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from articles.models import Article
from comments.forms import CommentForm
from comments.models import Comment

User = get_user_model()


def create_comment(request_data: QueryDict, user: User, article: Article):
    """Creates Comment"""
    if not user.is_authenticated:
        return
    comment_form = CommentForm(request_data)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.author = user
        new_comment.article = article
        if request_data.get('comment_id'):
            new_comment.parent = get_object_or_404(Comment,
                                                   pk=request_data.get('comment_id'))
        new_comment.save()