from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Articles, Like
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
    articles = Articles.objects.all().annotate(like_count=models.Count('like'))
    return render(request, 'post/article_list.html', {'articles' : articles})

def article_detail_view(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    

    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, article=article).exists()

    return render(request, 'post/article_detail.html', {
        'article': article,
        'is_liked': is_liked,
    })

def like_view(request, pk):
    if request.method == 'POST':
        print("요청 도착 ✅")
        print("로그인 여부:", request.user.is_authenticated)
        print("사용자:", request.user)
        article = get_object_or_404(Articles, pk=pk)
        like, created = Like.objects.get_or_create(user = request.user, article=article)

        if not created:     # 좋아요가 눌러져 있는 상태 -> 좋아요 취소
            like.delete()

        return redirect('article_detail', pk=pk)