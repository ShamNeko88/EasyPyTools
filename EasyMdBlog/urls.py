from django.urls import path
from .views import BlogIndexView


urlpatterns = [
    path("", BlogIndexView.as_view(), name="blog-index")
]
