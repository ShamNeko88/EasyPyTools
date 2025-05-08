from django.db import models


# アンケートヘッダ
class TranSurvey(models.Model):
    survey_id = models.AutoField(primary_key=True, null=False)  # 主キー
    title = models.CharField(max_length=100)  # アンケートタイトル
    detail = models.TextField()  # アンケート詳細
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'TRN_SURVEY'  # 実際のDBテーブル名を指定

    def __str__(self):
        return self.title

