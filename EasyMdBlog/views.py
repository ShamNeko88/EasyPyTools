from django.views.generic import TemplateView


class BlogIndexView(TemplateView):
    template_name = "EasyMdBlog/blog-index.html"
