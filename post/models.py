from ast import mod
from django.db import models
from django.contrib.auth import get_user_model
from myproject import settings
from multiselectfield import MultiSelectField

User = get_user_model()

TECH_STACKS = (
    ('Python', 'Python'),
    ('SpringBoot', 'SpringBoot'),
    ('Node.js', 'Node.js'),
    ('React', 'React'),
    ('TypeScript', 'TypeScript'),
    ('Kotlin', 'Kotlin'),
    ('Flutter', 'Flutter'),
    ('HTML/CSS/JS', 'HTML/CSS/JS'),
    ('MySQL', 'MySQL'),
)

class Articles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', null=False, blank=False)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField()
    photo = models.ImageField(upload_to='articles/photos/', blank=True)
    tech_stack = MultiSelectField(choices=TECH_STACKS, max_choices=9)
    github_link = models.URLField(blank=True)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)

class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.likes.count()

class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'comment')

class Search(models.Model):
    title = models.CharField(max_length=10)