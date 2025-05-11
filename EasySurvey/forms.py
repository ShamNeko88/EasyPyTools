from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from .models import TrnSurvey, TrnSurveyQuestion


class TrnSurveyForm(forms.ModelForm):
    class Meta:
        model = TrnSurvey
        fields = ["title", "detail"]  # 編集可能なフィールド


class CustomTrnSurveyQuestionFormSet(BaseInlineFormSet):
    def clean(self):
        """
        バリデーション時にquestion_idを無視する
        """
        for form in self.forms:
            if form.cleaned_data.get("DELETE"):
                continue
            # 必須フィールドのバリデーションをカスタマイズ
            if not form.cleaned_data.get("question"):
                form.add_error("question", "質問内容は必須です。")


# フォームセットの定義
TrnSurveyQuestionFormSet = inlineformset_factory(
    TrnSurvey,
    TrnSurveyQuestion,
    formset=CustomTrnSurveyQuestionFormSet,
    fields=["question"],  # 編集可能なフィールド
    extra=0,
    can_delete=True,
)
