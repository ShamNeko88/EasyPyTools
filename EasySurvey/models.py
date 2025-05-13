from typing import Any
from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User  # Userモデルをインポート


# アンケートヘッダ
class TrnSurvey(models.Model):
    survey_id = models.AutoField(primary_key=True)  # 主キー
    title = models.CharField(max_length=100)  # アンケートタイトル
    detail = models.TextField(null=True, blank=True)  # アンケート詳細
    access_token = models.CharField(max_length=36)  # アクセストークン
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )  # 作成者
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = "TRN_SURVEY"  # 実際のDBテーブル名を指定

    def __str__(self):
        return self.title


# アンケート内設問
class TrnSurveyQuestion(models.Model):
    survey_id = models.ForeignKey(
        TrnSurvey, on_delete=models.CASCADE, db_column="survey_id"
    )  # 外部キー
    question_id = models.AutoField(primary_key=True)  # 主キー
    show_choices_flag = models.CharField(max_length=1)  # 選択肢FLG
    question = models.CharField(max_length=100, null=True)  # 設問内容
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = "TRN_SURVEY_QUESTION"  # 実際のDBテーブル名を指定

    def __str__(self):
        return self.question  # 修正: 設問内容を返すように変更


# アンケート回答
class TrnSurveyAnswer(models.Model):
    # 回答内容の選択肢
    ANSWER_CHOICES = [
        (1, "〇"),
        (2, "△"),
        (3, "×"),
    ]
    survey_id = models.ForeignKey(
        TrnSurvey, on_delete=models.CASCADE, db_column="survey_id"
    )  # 外部キー
    question_id = models.ForeignKey(
        TrnSurveyQuestion, on_delete=models.CASCADE, db_column="question_id"
    )  # 外部キー
    answer_id = models.AutoField(primary_key=True)  # 主キー
    responder = models.CharField(max_length=50)
    answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)  # 回答内容
    comment = models.TextField(null=True)  # コメント（オプション）
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = "TRN_SURVEY_ANSWER"  # 実際のDBテーブル名を指定
        # ユニーク制約を追加
        constraints = [
            UniqueConstraint(
                fields=["survey_id", "question_id", "responder"],
                name="unique_survey_question_responder",  # ユニーク制約の名前
            )
        ]

    def __str__(self):
        return f"回答者: {self.responder}, 質問: {self.question_id.question}, 回答: {self.get_answer_display()}"
