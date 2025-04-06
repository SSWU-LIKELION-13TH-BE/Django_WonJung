from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Articles

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'content', 'photo', 'tech_stack', 'github_link']
        widget = {
            'teck_stack' : forms.CheckboxSelectMultiple(),
        }

    