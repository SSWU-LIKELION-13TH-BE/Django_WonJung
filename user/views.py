from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login

from .models import CustomUser
from post.models import Articles
from .forms import GuestbookForm, SignUpForm, LoginForm, UserUpdateForm
from django.core.mail.message import EmailMessage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = LoginForm()
        
    return render(request, 'user/login.html', {'form' : form})

def logout_view(request):
    logout(request)
    return redirect('login')

def main_view(request):
    return render(request, 'main.html')

def change_password_view(request):
    if request.method == "POST" :
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully changed')
            return redirect('main')
        else:
            messages.error(request, 'Password not changed')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'user/change_password.html', {'form' : form})

def mypage_view(request):
    user = request.user

    # 내가 올린 게시물 조회
    my_posts = Articles.objects.filter(author=user).order_by('-id')     # 게시물은 최신순으로 정렬
    return render(request, 'user/mypage.html', {'my_posts' : my_posts})

def edit_profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mypage')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'user/edit_profile.html', {'form' : form})

def guestbook_view(request, user_id):
    
    owner = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = GuestbookForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.owner = owner          # 수신자 지정
            entry.author = request.user  # 작성자 지정
            entry.save()
            return redirect('guestbook', user_id=owner.id)
    else:
        form = GuestbookForm()

    return render(request, 'user/guestbook.html', {
        'form': form,
        'owner': owner
    })
