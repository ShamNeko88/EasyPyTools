from django.views.generic import (
    TemplateView, CreateView, UpdateView
)


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, EmailSettingForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView


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


# パスワード変更
class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_done')  # 完了ページのURL
    success_message = "パスワードが変更されました。"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


# パスワード変更完了画面
class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/password_change_done.html'


# メールアドレス設定
class EmailSettingView(LoginRequiredMixin, UpdateView):
    form_class = EmailSettingForm
    template_name = 'TopPage/email_setting.html'
    success_url = reverse_lazy('email_setting')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'メールアドレスを更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'メールアドレスの更新に失敗しました。')
        return super().form_invalid(form)
