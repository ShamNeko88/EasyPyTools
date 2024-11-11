from django.urls import path
from .views import IndexView


urlpatterns = [
    path("EasyLiveMemo", IndexView.as_view(), name="EasyLiveMemo")
]
