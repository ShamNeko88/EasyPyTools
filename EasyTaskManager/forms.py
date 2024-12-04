# EasyTaskManager/forms.py

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'status']  # 優先度とステータスを含める