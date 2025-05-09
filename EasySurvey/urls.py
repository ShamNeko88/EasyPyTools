from django.urls import path
from .views import SurveyIndexView, SurveyAnswerView, SurveyResultView

urlpatterns = [
    path("", SurveyIndexView.as_view(), name="survey-index"),
    path(
        "answer/<str:access_token>/", SurveyAnswerView.as_view(), name="survey-answer"
    ),
    path(
        "survey/<str:access_token>/result/",
        SurveyResultView.as_view(),
        name="survey_result",
    ),
]
