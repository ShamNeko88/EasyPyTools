from django.views.generic import (
    TemplateView
)


class SurveyIndexView(TemplateView):
    template_name = "EasySurvey/survey-index.html"
