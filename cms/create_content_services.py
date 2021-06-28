from typing import Any

from django.apps import apps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.base import ModelBase
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDict
from django.contrib.auth import get_user_model
from articles.models import Content, Article


User = get_user_model()


def delete_content(content_id: int, user: User):
    """Deletes Content"""
    Content.objects.filter(id=content_id,
                           article__user=user).delete()


def get_model(model_name: str):
    """Returns model by her names"""
    if model_name in ['text', 'video', 'image', 'file', 'title']:
        return apps.get_model(app_label='articles',
                              model_name=model_name)
    return None


def get_form(model: ModelBase, *args, **kwargs):
    """Returns Form that is generated from Model"""
    form = modelform_factory(model, exclude=['owner',
                                             'order',
                                             'created',
                                             'updated'])
    return form(*args, **kwargs)


def get_file_for_create_item(file: InMemoryUploadedFile) -> MultiValueDict:
    """Converts InMemoryUploadedFile to MultiValueDict with key 'file'"""
    return MultiValueDict({'file': [file]})


def validation_and_item_creation(form: Any, user: User):
    """Checks form for validity and saves Item in database"""
    if form.is_valid():
        item_obj = form.save(commit=False)
        item_obj.owner = user
        item_obj.save()
        return item_obj
    return None


def content_create_or_update(article: Article, order: int, user: User, content_id: int = None, item_obj: Any = None):
    """Creates or updates Content"""
    if not content_id:
        Content.objects.create(article=article,
                               item=item_obj,
                               order=order)
    else:
        Content.objects.filter(id=content_id,
                               article__user=user).update(order=order)


def manage_text_content(request_data: dict, user: User, article: Article = None):
    """Processes article Content containing Title or Text fields"""
    for index, data in request_data.items():
        if data['delete']:
            delete_content(content_id=data['content_id'],
                           user=user)
            continue
        if not article:
            article = get_object_or_404(Article,
                                        id=data['article_id'],
                                        user=user)
        item_obj = None
        model = get_model(model_name=data['item_type'])
        if data['old_item']:
            item_obj = get_object_or_404(model,
                                         id=data['item_id'],
                                         owner=user)
        form = get_form(model,
                        instance=item_obj,
                        data=data)
        item_obj = validation_and_item_creation(form=form,
                                                user=user)
        if item_obj:
            if not data['content_id']:
                content_create_or_update(article=article,
                                         order=data['order'],
                                         user=user,
                                         content_id=None,
                                         item_obj=item_obj)
            else:
                content_create_or_update(article=article,
                                         order=data['order'],
                                         user=user,
                                         content_id=data['content_id'],
                                         item_obj=item_obj)
    return article


def manage_image_content(request_data: dict, user: User, files: MultiValueDict, article: Article = None):
    """Processes article Content containing Image fields"""
    for index, data in request_data.items():
        if 'delete' in data:
            delete_content(content_id=int(data[2]),
                           user=user)
            continue
        elif 'adding' in data:
            model = get_model(model_name='image')
            if not article:
                article = get_object_or_404(Article,
                                            id=int(data[0]),
                                            user=user)
            file = get_file_for_create_item(files[index])
            form = get_form(model,
                            data=request_data,
                            files=file)
            item_obj = validation_and_item_creation(form=form,
                                                    user=user)
            content_create_or_update(article=article,
                                     order=int(data[1]),
                                     user=user,
                                     content_id=None,
                                     item_obj=item_obj)
        else:
            content_create_or_update(article=article,
                                     order=int(data[1]),
                                     user=user,
                                     content_id=int(data[2]),
                                     item_obj=None)
    return article
