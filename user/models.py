from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

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