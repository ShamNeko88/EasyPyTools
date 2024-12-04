# EasyTaskManager/views.py

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

class TaskManagerView(View):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)  # ログインユーザーのタスクを取得
        form = TaskForm()  # 新しいタスク用のフォームを作成
        return render(request, 'EasyTaskManager/task-index.html', {'tasks': tasks, 'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # ログインユーザーを設定
            task.save()
            return redirect('task-index')  # タスク一覧にリダイレクト
        return render(request, 'EasyTaskManager/task-index.html', {'form': form})

class TaskDeleteView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('task-index')  # タスク一覧にリダイレクト