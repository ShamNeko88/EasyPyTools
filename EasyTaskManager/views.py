import datetime

from django.shortcuts import render, redirect
from django.views import View
from .models import Task
from .forms import TaskForm


class TaskManagerView(View):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        today_tasks = Task.objects.filter(user=request.user, due_date=datetime.date.today())
        ideas = Task.objects.filter(user=request.user, is_idea=True)
        form = TaskForm()

        return render(request, 'EasyTaskManager/task-index.html', {
            'tasks': tasks,
            'today_tasks': today_tasks,
            'ideas': ideas,
            'form': form,
        })

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # ユーザーを設定
            task.save()
            return redirect('task-index')  # タスク管理ページにリダイレクト
        return self.get(request)  # エラーがあれば再表示


# 優先タスク
class TaskPriorityView(View):
    def get(self, request):
        # ユーザーの優先タスクを取得
        priority_tasks = Task.objects.filter(user=request.user, is_priority=True)
        form = TaskForm()

        return render(request, 'EasyTaskManager/task-priority.html', {
            'tasks': priority_tasks,
            'form': form,
        })

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # ユーザーを設定
            task.save()
            return redirect('task-priority')  # 優先タスクページにリダイレクト
        return self.get(request)  # エラーがあれば再表示
    