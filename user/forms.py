from encodings.punycode import T
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

# 회원정보(닉네임/비밀번호) 수정
class UserUpdateForm(forms.ModelForm):
    new_pw = forms.CharField(
        label='new password',
        widget=forms.PasswordInput,
        required=False,
        help_text= "비밀번호를 변경하려면 입력하세요." 
    )

    class Meta:
        model = CustomUser
        fields=['nickname']     # 닉네임 수정
    
    def save(self, commit=True):
        user = super().save(commit=False)
        new_pw = self.cleaned_data.get('new_pw')

        if new_pw:
            user.set_password(new_pw)
        
        if commit:
            user.save()
        
        return user
