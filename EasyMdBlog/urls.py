from django.urls import path
from .views import (
    BlogIndexView, BlogPostDetail, BlogPostCreate, BlogPostUpdate
)

urlpatterns = [
    path("", BlogIndexView.as_view(), name="blog-index"),
    path("post/<int:pk>/", BlogPostDetail.as_view(), name="post-detail"),
    path("post/new/", BlogPostCreate.as_view(), name="post-create"),
    path("post/<int:pk>/edit/", BlogPostUpdate.as_view(), name="post-edit"),
]
