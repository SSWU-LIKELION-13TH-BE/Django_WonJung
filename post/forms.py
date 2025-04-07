from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Articles, Comment

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'content', 'photo', 'tech_stack', 'github_link']
        widget = {
            'teck_stack' : forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widget = {
            'content' : forms.Textarea(attrs={'rows' : 3, 'placeholder' : '댓글을 입력해 주세요.'}),
        }
