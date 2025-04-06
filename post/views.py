from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Articles
from .forms import ArticleCreateForm

@login_required
def create_view(request):
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleCreateForm()
    return render(request, 'post/article_create.html', {'form': form})

def article_list_view(request):
    articles = Articles.objects.all()
    return render(request, 'post/article_list.html', {'articles' : articles})

def article_detail_view(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    return render(request, 'post/article_detail.html', {'article' : article})