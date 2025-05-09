from django.urls import path
from .views import (
    SurveyIndexView,
    SurveyAnswerView
)

urlpatterns = [
    path("", SurveyIndexView.as_view(), name="survey-index"),
    path("answer/<str:access_token>/", SurveyAnswerView.as_view(), name="survey-answer"),
]
