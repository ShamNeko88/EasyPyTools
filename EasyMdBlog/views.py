from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import BlogPost
from django.utils.html import mark_safe
import bleach


# ブログ一覧ページ
class BlogIndexView(ListView):
    model = BlogPost
    template_name = "EasyMdBlog/blog-index.html"
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset


# ブログの詳細閲覧ページ
class BlogPostDetail(DetailView):
    model = BlogPost
    template_name = "EasyMdBlog/blog-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        markdown_content = self.object.content
        # bleachを使用してHTMLをサニタイズ
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'ul', 'ol', 'li'
        ]
        clean_content = bleach.clean(markdown_content, tags=allowed_tags)

        context['content'] = mark_safe(clean_content)  # Djangoのテンプレートで安全に表示
        return context


# ブログの新規作成ページ
class BlogPostCreate(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content',]
    template_name = 'EasyMdBlog/post-form.html'
    success_url = reverse_lazy('blog-index')

    def form_valid(self, form):
        # form.instance.user に現在のログインユーザーをセット
        form.instance.user = self.request.user
        return super().form_valid(form)


# ブログの編集ページ
class BlogPostUpdate(LoginRequiredMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'EasyMdBlog/blog-post.html'
    success_url = reverse_lazy('my-posts')


# マイページ（自分の投稿一覧）
class MyBlogListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = "EasyMdBlog/my-posts.html"
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = BlogPost.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset


# ブログの削除
class BlogPostDelete(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'EasyMdBlog/blog-delete.html'
    success_url = reverse_lazy('my-posts')  # 削除後のリダイレクト先