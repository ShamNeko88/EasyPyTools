# EasyTaskManager/urls.py

from django.urls import path
from .views import TaskManagerView, TaskDeleteView

urlpatterns = [
    path("", TaskManagerView.as_view(), name="task-index"),  # タスク一覧と追加用のURL
    path("task/delete/<int:pk>/", TaskDeleteView.as_view(), name="task-delete"),  # タスク削除用のURL
]