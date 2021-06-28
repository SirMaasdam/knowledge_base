from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list_view, name='articles'),
    path('articles/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.article_detail_view, name='detail')
]
