from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.urls import reverse
from pytils.translit import slugify

from articles.auxiliary_functions import create_slug_code
from articles.fields import OrderField


User = get_user_model()


class OnModerationManager(models.Manager):
    """Custom manager for Article where draft == false"""
    def get_queryset(self):
        return super().get_queryset().filter(draft=False)


class Article(models.Model):
    """Article Model"""
    user = models.ForeignKey(User,
                             verbose_name='Автор',
                             on_delete=models.CASCADE,
                             related_name='articles')
    title = models.CharField(verbose_name='Название статьи',
                             max_length=255)
    slug = models.SlugField(max_length=255,
                            unique=True)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    draft = models.BooleanField(default=True)
    objects = models.Manager()
    published = OnModerationManager()

    def save(self, *args, **kwargs):
        """Redefining the method for adding a slug"""
        if not self.slug:
            self.slug = f'{slugify(self.title)}-{create_slug_code(3)}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Absolute url for simple viewing"""
        return reverse('articles:detail',
                       args=[self.created.year,
                             self.created.month,
                             self.created.day,
                             self.slug])

    def get_absolute_url_for_manage(self):
        """Absolute url for manage"""
        return reverse('cms:detail',
                       args=[self.slug])

    def get_comment(self):
        """Returns the main comment in the branch"""
        return self.comments.filter(parent__isnull=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-created']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Content(models.Model):
    """Model for creating article content"""
    article = models.ForeignKey(Article,
                                related_name='contents',
                                on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file',
                                         'citation',
                                         'title')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['article'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    """
    Abstract class
    Basic content model of article content
    """
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE,
                              verbose_name='items')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.owner

    def get_type(self):
        """Returns model name"""
        return self._meta.model_name

    def render_to_show(self):
        """Renders a template with one of the content types to display"""
        return render_to_string(f'../../articles/templates/content/{self._meta.model_name}.html',
                                {'item': self})

    def render_to_manage(self):
        """Renders a template with one of the content types to manage"""
        return render_to_string(f'../../cms/templates/content/{self._meta.model_name}.html',
                                {'item': self})


class Title(ItemBase):
    """Extension of the basic content model of the article content that has the title format"""
    content = models.CharField(max_length=255)


class Text(ItemBase):
    """Extension of the basic content model of the article content that has the text format"""
    content = models.TextField()


class File(ItemBase):
    """Extension of the basic content model of the article content that has the file format"""
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """Extension of the basic content model of the article content that has the image format"""
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    """Extension of the basic content model of the article content that has the url format"""
    url = models.URLField()


class Citation(ItemBase):
    """Extension of the basic content model of the article content that has the citation format"""
    content = models.TextField()
    signature = models.TextField()
