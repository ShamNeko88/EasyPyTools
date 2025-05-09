from django.db import models


# アンケートヘッダ
class TrnSurvey(models.Model):
    survey_id = models.AutoField(primary_key=True)  # 主キー
    title = models.CharField(max_length=100)  # アンケートタイトル
    detail = models.TextField(null=True)  # アンケート詳細
    access_token = models.CharField(max_length=36)  # アクセストークン
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'TRN_SURVEY'  # 実際のDBテーブル名を指定

    def __str__(self):
        return self.title


# アンケート内設問
class TrnSurveyQuestion(models.Model):
    survey_id = models.ForeignKey(
        TrnSurvey, on_delete=models.CASCADE, db_column="survey_id"
    )  # 外部キー
    question_id = models.AutoField(primary_key=True)  # 主キー
    question = models.CharField(max_length=100)  # 設問内容
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'TRN_SURVEY_QUESTION'  # 実際のDBテーブル名を指定

    def __str__(self):
        return self.survey_id


# アンケート回答
class TrnSurveyAnswer(models.Model):
    survey_id = models.ForeignKey(
        TrnSurvey, on_delete=models.CASCADE, db_column="survey_id"
    )  # 外部キー
    question_id = models.ForeignKey(
        TrnSurveyQuestion, on_delete=models.CASCADE, db_column="question_id"
    )  # 外部キー
    answer_id = models.AutoField(primary_key=True)  # 主キー
    responder = models.CharField(max_length=50)
    answer = models.CharField(max_length=1)  # 回答内容
    comment = models.TextField(null=True)  # コメント（オプション）
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'TRN_SURVEY_ANSWER'  # 実際のDBテーブル名を指定
        unique_together = ('survey_id', 'question_id', 'responder')  # 一意性を確保（複合主キーのようなもの）

    def __str__(self):
        return self.answer_id
