from http.client import HTTPResponse
import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
import urllib
import logging

from myproject import settings
from myproject.settings import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

from .models import CustomUser, Guestbook
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
    guestbooks = Guestbook.objects.filter(owner=owner)

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
        'owner': owner,
        'guestbooks': guestbooks
    })

NAVER_CLIENT_ID = settings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET
NAVER_CALLBACK_URI = "http://127.0.0.1:8000/accounts/naver/login/callback/"

logger = logging.getLogger(__name__)

# 네이버 소셜 로그인
def naver_login_view(request):
    client_id = NAVER_CLIENT_ID
    redirect = urllib.parse.quote(NAVER_CALLBACK_URI)
    auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={urllib.parse.quote(NAVER_CALLBACK_URI)}"
        f"&state=naver_login"
    )

    return redirect(auth_url)

# 네이버 로그인 콜백
def naver_callback_view(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    # Access Token 요청
    token_url = "https://nid.naver.com/oauth2.0/token"
    token_data = {
        'grant_type': "authorization_code",
        'client_id': NAVER_CLIENT_ID,
        'client_secret': NAVER_CLIENT_SECRET,
        'code': code,
        'state': state,
    }

    response = requests.post(token_url, data=token_data)
    logger.info(f"Token Response: {response.status_code} - {response.text}")

    if response.status_code != 200:
        logger.error(f"Access Token Error: {response.text}")
        return redirect('login')

    token = response.json()
    access_token = token.get('access_token')

    if not access_token:
        logger.error("Access Token could not be retrieved.")
        return redirect('login')

    # 사용자 정보 요청
    user_info_url = "https://openapi.naver.com/v1/nid/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    user_info_response = requests.get(user_info_url, headers=headers)
    logger.info(f"User Info Response: {user_info_response.status_code} - {user_info_response.text}")

    if user_info_response.status_code != 200:
        logger.error("Failed to retrieve user information.")
        return redirect('login')

    user_info = user_info_response.json()
    naver_id = user_info.get('response', {}).get('id')
    nickname = user_info.get('response', {}).get('nickname')
    email = user_info.get('response', {}).get('email')
    name = user_info.get('response', {}).get('name')

    if not naver_id or not email:
        logger.error("Naver user information could not be retrieved.")
        return redirect('login')

    # 기존 사용자 확인
    user = CustomUser.objects.filter(email=email).first()
    
    if user:
        logger.info("Existing user found, logging in.")
        # 이미 존재하는 사용자의 경우 네이버 ID가 설정되어 있지 않다면 설정
        if not user.naver_id:
            user.naver_id = naver_id
            user.save()
    else:
        # 새로운 사용자 생성
        user = CustomUser.objects.create(
            email=email,
            naver_id=naver_id,
            nickname=nickname,
            username=email,
            first_name=name
        )
        logger.info("New user created.")

    # 사용자 로그인 처리
    login(request, user)
    logger.info(f"User {'created' if user.naver_id == naver_id else 'logged in'}: {user}")

    return redirect('main')  # 로그인 후 메인 페이지로 리다이렉트


def kakao_login_view(request):
    redirect_uri = "http://127.0.0.1:8000/user/kakao/callback"
    kakao_client_id = conf.KAKAO_CLIENT_ID
    kakao_login_url= f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={kakao_client_id}&redirect_uri={redirect_uri}"

    return redirect(kakao_login_url)

def kakao_callback_view(request):
    
    code = request.GET.get('code')

    if not code:
        return HTTPResponse('Code not found', status=400)

    # 카카오 API에 access_token을 요청하는 코드
    kakao_token_url = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': conf.KAKAO_CLIENT_ID,  # 카카오 앱의 REST API 키
        'redirect_uri': 'http://127.0.0.1:8000/accounts/kakao/login/callback',
        'code': code,
    }

    response = request.post(kakao_token_url, data=data)
    token_data = response.json()

    # print(f"Response from Kakao token API: {token_data}")   # 토큰 제대로 받고 있나 확인

    if 'access_token' not in token_data:
        return HTTPResponse('Failed to get access token', status=400)

    access_token = token_data['access_token']

    # 카카오 사용자 정보 가져오기
    kakao_user_info_url = 'https://kapi.kakao.com/v2/user/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    user_info_response = request.get(kakao_user_info_url, headers=headers)
    user_info = user_info_response.json()


    # 필요한 데이터 추출
    kakao_id = user_info['id']
    nickname = user_info.get('properties', {}).get('nickname', '')
    email = user_info.get('kakao_account', {}).get('email', '')


    if not email:
        email = None


    # 카카오 ID로 사용자 찾기 또는 새로 생성
    user, created = CustomUser.objects.get_or_create(
        kakao_id=kakao_id,
        defaults={
            'username': nickname,
            'nickname': nickname,
            'email' : email,
        }
    )

    # 만약 사용자가 이미 존재하면 정보 업데이트
    if not created:
        user.save()

    login(request, user)

    return redirect('user:home')
