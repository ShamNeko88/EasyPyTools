from django.urls import path
from .views import TaskManagerView, TaskPriorityView, TaskUpdateView, TaskIdeaView

urlpatterns = [
    path("", TaskManagerView.as_view(), name="task-index"),
    path("task-priority", TaskPriorityView.as_view(), name="task-priority"),
    path("task-idea", TaskIdeaView.as_view(), name="task-idea"),
    path("update/<int:task_id>/", TaskUpdateView.as_view(), name="task-update"),  # 更新用のURL
]
