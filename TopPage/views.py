from django.views.generic import (
    TemplateView
)


# ルート
class IndexView(TemplateView):
    template_name = "TopPage/index.html"
