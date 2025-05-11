from django.urls import path
from .views import (
    SurveyIndexView,
    SurveyAnswerView,
    SurveyResultView,
    SurveyListView,
    SurveyCompleteView,
    SurveyDeleteView,
    SurveyEditView,
    QuestionDeleteView,
)

urlpatterns = [
    path("", SurveyIndexView.as_view(), name="survey-index"),
    path(
        "answer/<str:access_token>/", SurveyAnswerView.as_view(), name="survey-answer"
    ),
    path(
        "survey/<str:access_token>/result/",
        SurveyResultView.as_view(),
        name="survey-result",
    ),
    path("my-surveys/", SurveyListView.as_view(), name="survey-list"),
    path(
        "survey/complete/<str:access_token>/",
        SurveyCompleteView.as_view(),
        name="survey-complete"
    ),
    path("list/", SurveyListView.as_view(), name="survey-list"),
    path("delete/<int:pk>/", SurveyDeleteView.as_view(), name="survey-delete"),
    path("survey/<int:pk>/edit/", SurveyEditView.as_view(), name="survey-edit"),
    path('question/delete/<int:pk>/', QuestionDeleteView.as_view(), name='question-delete'),
]
