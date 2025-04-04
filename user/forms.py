from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)     # e-mail 필수

    class Meta:
        model = CustomUser
        # fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        fields = ['id', 'nickname', 'email', 'password1', 'password2']      # week2 과제 수정

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['id', 'password']