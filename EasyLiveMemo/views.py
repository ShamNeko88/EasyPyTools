from django.views.generic import (
    TemplateView
)


# ルート
class IndexView(TemplateView):
    template_name = "EasyLiveMemo/memo-index.html"
