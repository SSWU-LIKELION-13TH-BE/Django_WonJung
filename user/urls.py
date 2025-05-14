from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('main/', main_view, name='main'),

    path('change_password/', change_password_view, name='change_password'),

    path('mypage/', mypage_view, name='mypage'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('<str:user_id>/guestbook/', guestbook_view, name='guestbook'),


    # 비밀번호 재설정
    # 템플릿 오버라이딩 추가
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),

    # 소셜 로그인
    path('accounts/naver/login/', naver_login_view, name='naver_login'),
    path('accounts/naver/callback/', naver_callback_view, name='naver_callback'),

    path('kakao/login/', kakao_login_view, name='kakao_login'),
    path('kakao/callback/', kakao_callback_view, name='kakao_callback'),
    
]