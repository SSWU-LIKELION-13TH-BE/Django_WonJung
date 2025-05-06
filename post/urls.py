from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_view, name='article_create'),
    path('list/', article_list_view, name='article_list'),
    path('<int:pk>/', article_detail_view, name='article_detail'),
    path('<int:pk>/like', like_view, name='like'),
    path('comment/<int:comment_id>/like/', comment_like_view, name='comment_like'),

    # 게시물 수정 및 삭제
    path('article/<int:pk>/edit', article_edit_view, name='article_edit'),
    path('article/<int:pk>/delete', article_delete_view, name='article_delete')

]