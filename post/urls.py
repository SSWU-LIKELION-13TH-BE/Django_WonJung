from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_view, name='article_create'),
    path('list/', article_list_view, name='article_list'),
    path('<int:pk>/', article_detail_view, name='article_detail'),
    path('<int:pk>/like', like_view, name='like')
]