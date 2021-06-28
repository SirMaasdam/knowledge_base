from django.db import models
from django.contrib.auth import get_user_model
from articles.models import Article


User = get_user_model()


class Comment(models.Model):
    """Model for comments to the Article"""
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='comments')
    article = models.ForeignKey(Article,
                                verbose_name='Название статьи',
                                on_delete=models.CASCADE,
                                related_name='comments')
    parent = models.ForeignKey('self',
                               verbose_name='Главный комментарий',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='child_comments')
    message = models.TextField(verbose_name='Коммантарий')
    active = models.BooleanField(default=True,
                                 verbose_name='Активен')

    def __str__(self):
        return f'Комментарий автора {self.author.username}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

