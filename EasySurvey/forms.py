from django import forms
from .models import TrnSurvey, TrnSurveyQuestion
from django.forms.models import inlineformset_factory


class TrnSurveyForm(forms.ModelForm):
    class Meta:
        model = TrnSurvey
        fields = ["title", "detail"]  # 編集可能なフィールド


# TrnSurveyに関連するTrnSurveyQuestionを編集するためのフォームセット
TrnSurveyQuestionFormSet = inlineformset_factory(
    TrnSurvey,
    TrnSurveyQuestion,
    fields=["question"],
    extra=1,  # 新しい質問を追加できるようにする
    can_delete=True,  # 質問を削除できるようにする
)
