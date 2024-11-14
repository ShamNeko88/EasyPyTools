from django.urls import path
from .views import (
    BlogIndexView, BlogPostDetail, BlogPostCreate, BlogPostUpdate,
    MyBlogListView, BlogPostDelete
)

urlpatterns = [
    path("", BlogIndexView.as_view(), name="blog-index"),
    path("my-posts/", MyBlogListView.as_view(), name="my-posts"),  # 追加
    path("post/<int:pk>/", BlogPostDetail.as_view(), name="post-detail"),
    path("post/new/", BlogPostCreate.as_view(template_name='EasyMdBlog/blog-post.html'), name="post-create"),
    path("post/<int:pk>/edit/", BlogPostUpdate.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", BlogPostDelete.as_view(), name="post-delete"),
]
