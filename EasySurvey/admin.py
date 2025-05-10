"""管理サイトで管理するための設定を行うファイル
ここで定義すると、Djangoの管理サイトでモデルを管理できるようになる
"""

from django.contrib import admin
from .models import TrnSurvey, TrnSurveyQuestion, TrnSurveyAnswer

# Register your models here.
admin.site.register(TrnSurvey)
admin.site.register(TrnSurveyQuestion)


@admin.register(TrnSurveyAnswer)
class TrnSurveyAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "responder", "survey_id", "question_id", "answer", "created_at",
        "updated_at", "comment"
    )
