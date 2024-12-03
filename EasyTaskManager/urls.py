from django.urls import path
from .views import TaskManagerView, TaskPriorityView

urlpatterns = [
    path("", TaskManagerView.as_view(), name="task-index"),
    path("task-priority", TaskPriorityView.as_view(), name="task-priority")
]
