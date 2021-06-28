from django import template

from articles.models import Article

register = template.Library()


@register.inclusion_tag('templatetags/article_description.html')
def show_post_description(article: Article):
    """Render first Image and firs Text of Article"""
    img = return_item(article=article,
                      content_type='image')
    text = return_item(article=article,
                       content_type='text')
    return {'img': img,
            'text': text}


def return_item(article: Article, content_type: str):
    """Returns first Item of this type found in Article"""
    try:
        return article.contents.filter(content_type__model=content_type)[0]
    except IndexError:
        return None