from django.urls import path
from .views import IndexView, RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # 認証関連のURL
    path('login/', auth_views.LoginView.as_view(template_name='TopPage/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='TopPage/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='TopPage/password_change_done.html'), name='password_change_done'),
]
