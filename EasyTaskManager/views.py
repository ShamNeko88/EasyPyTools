import datetime

from django.shortcuts import render, redirect
from django.views import View
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse  # AJAX


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


class TaskUpdateView(View):
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id, user=request.user)
        task.is_completed = request.POST.get('is_completed') == 'on'
        task.is_priority = request.POST.get('is_priority') == 'on'
        task.is_idea = request.POST.get('is_idea') == 'on'
        task.save()
        return JsonResponse({'success': True})


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


# 思考中
class TaskIdeaView(View):
    def get(self, request):
        # ユーザーの思考中のタスクを取得
        idea_tasks = Task.objects.filter(user=request.user, is_idea=True)
        form = TaskForm()

        return render(request, 'EasyTaskManager/task-idea.html', {
            'tasks': idea_tasks,
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
