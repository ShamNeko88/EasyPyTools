from django.views.generic import (
    TemplateView, CreateView
)


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm


# ルート
class IndexView(TemplateView):
    template_name = "TopPage/index.html"


# ユーザー登録
class RegisterView(CreateView):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'TopPage/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 自動的にログイン
            return redirect('index')  # 登録後のリダイレクト先
        return render(request, 'TopPage/register.html', {'form': form})
