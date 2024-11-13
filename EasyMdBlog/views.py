from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import BlogPost
import markdown
import bleach
from django.utils.safestring import mark_safe


# ブログ一覧ページ
class BlogIndexView(ListView):
    model = BlogPost
    template_name = "EasyMdBlog/blog-index.html"
    context_object_name = 'posts'


# ブログの詳細閲覧ページ
class BlogPostDetail(DetailView):
    model = BlogPost
    template_name = "EasyMdBlog/post-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # シンプルな設定
        md = markdown.Markdown(extensions=['extra'])
        html = md.convert(self.object.content)

        # 基本的なタグのみ許可
        allowed_tags = [
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'a', 'ul', 'ol', 'li', 'code', 'pre',
            'strong', 'em', 'blockquote'
        ]
        allowed_attrs = {
            'a': ['href', 'title']
        }

        clean_html = bleach.clean(
            html,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )

        context['content'] = mark_safe(clean_html)
        return context


class BlogPostCreate(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content',]
    template_name = 'EasyMdBlog/post-form.html'
    success_url = reverse_lazy('blog-index')

    def form_valid(self, form):
        # form.instance.user に現在のログインユーザーをセット
        form.instance.user = self.request.user
        return super().form_valid(form)


class BlogPostUpdate(LoginRequiredMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'user']
    template_name = 'EasyMdBlog/post-form.html'
    success_url = reverse_lazy('blog-index')
