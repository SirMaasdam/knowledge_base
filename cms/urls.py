from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.article_manage_list_view, name='manage'),
    path('create/', views.articles_create_view, name='create'),
    path('create_content/', views.create_update_delete_content_view, name='create_content'),
    path('create_image_content/', views.create_update_delete_content_with_file_view, name='create_image_content'),
    path('<slug:slug>/', views.article_manage_detail_view, name='detail'),
]
