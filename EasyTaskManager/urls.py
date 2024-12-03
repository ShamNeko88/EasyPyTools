from django.urls import path
from .views import TaskManagerView, TaskPriorityView, TaskUpdateView

urlpatterns = [
    path("", TaskManagerView.as_view(), name="task-index"),
    path("task-priority", TaskPriorityView.as_view(), name="task-priority"),
    path("update/<int:task_id>/", TaskUpdateView.as_view(), name="task-update"),  # 更新用のURL
]
