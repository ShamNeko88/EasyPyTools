# EasyTaskManager/models.py

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('completed', '完了'),
        ('incomplete', '未完了'),
        ('pending', '保留'),
    ]

    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.BooleanField(default=False)  # 優先タスク
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='incomplete')  # ステータス

    def __str__(self):
        return self.title