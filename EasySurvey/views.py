from django.views.generic import (
    TemplateView
)


# 初期ページ（アンケート作成）
class SurveyIndexView(TemplateView):
    template_name = "EasySurvey/survey-index.html"


# アンケート回答ページ
class SurveyAnswerView(TemplateView):
    template_name = "EasySurvey/survey-answer.html"
