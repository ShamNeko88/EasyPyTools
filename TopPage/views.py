from django.views.generic import (
    TemplateView
)
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


# ルート
class IndexView(TemplateView):
    template_name = "TopPage/index.html"


# ユーザー登録
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'TopPage/register.html'
    success_url = reverse_lazy('login')
