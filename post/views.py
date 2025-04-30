from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Articles, Comment, CommentLike, Like
from .forms import ArticleCreateForm, CommentForm, SearchForm

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
    sort = request.GET.get('sort', 'recent')  # default값 : 최신순
    query = ''
    articles = Articles.objects.all()
    # articles = Articles.objects.annotate(like_count=Count('like'))

    # 게시물 검색 기능
    form = SearchForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data['title']
        articles = Articles.objects.filter(title__icontains=title)
    else:
        articles = Articles.objects.all()
    
    # 정렬 적용
    if sort == 'popular':
        articles = articles.annotate(like_count=Count('like')).order_by('-like_count', '-id')
    else:  # 기본: 최신순
        articles = articles.order_by('-id')

    return render(request, 'post/article_list.html', {
        'articles': articles,
        'query': query,
        'sort': sort,
    })

def article_detail_view(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    comments = article.comments.filter(parent__isnull=True).order_by('-created_at')
    
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, article=article).exists()

    comment_likes = {}      # 댓글 좋아요 개수
    for comment in article.comments.all():
        comment_likes[comment.id] = comment.likes.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'post/article_detail.html', {
        'article': article,
        'is_liked': is_liked,
        'comments' : comments,
        'form' : form,
        'comment_likes': comment_likes,
    })

def like_view(request, pk):
    if request.method == 'POST':
        article = get_object_or_404(Articles, pk=pk)
        like, created = Like.objects.get_or_create(user = request.user, article=article)

        if not created:     # 좋아요가 눌러져 있는 상태 -> 좋아요 취소
            like.delete()

        return redirect('article_detail', pk=pk)

def comment_like_view(request, comment_id):
    comment = get_object_or_404(Comment, id = comment_id)

    if request.method == 'POST':
        like, created = CommentLike.objects.get_or_create(user = request.user, comment=comment)

        if not created:
            like.delete()
        
        return redirect('article_detail', pk=comment.article.pk)
