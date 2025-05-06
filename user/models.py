from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from myproject import settings

class CustomUser(AbstractUser):
    # phone_number = models.CharField(max_length=15, blank = True, null = True)

    # week2 과제
    nickname = models.CharField(max_length=15, blank = False, null = False, default='')
    id = models.CharField(max_length=15, blank=False, null = False, primary_key=True)
    username = None

    groups = models.ManyToManyField(Group, related_name = "customer_set", blank = True)
    user_permissions = models.ManyToManyField(Permission, related_name="customer_permission_set", blank=True)

    # week2 과제 - id를 primary key로 설정함
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = 'nickname', 'email'

class Guestbook(models.Model):
    # 방명록을 받은 유저 (사용자 본인)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='guestbook_received'
    )

    # 방명록 작성자
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='guestbook_written'
    )

    message = models.TextField()        # 방명록 내용
    createdAt = models.DateTimeField(auto_now_add=True)
        