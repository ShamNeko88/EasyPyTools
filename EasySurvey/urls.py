from django.urls import path
from .views import (
    SurveyIndexView
)

urlpatterns = [
    path("", SurveyIndexView.as_view(), name="survey-index")
]
