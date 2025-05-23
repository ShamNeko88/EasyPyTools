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


class TrnSurveyQuestionForm(forms.ModelForm):
    show_choices_flag = forms.BooleanField(
        label='〇, △, ×の選択肢を表示',
        required=False,
    )

    class Meta:
        model = TrnSurveyQuestion
        fields = ["question", "show_choices_flag"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # データベースから"show_choices_flag"の値を取得
        value = getattr(self.instance, "show_choices_flag", "1")
        # チェックボックスの初期値をセット
        self.fields["show_choices_flag"].initial = (value == "1")
        print("DEBUG:", self.instance.question, value, (value == "1"))
    # formから受け取った値をデータベースに保存するための値に変換
    def clean_show_choices_flag(self):
        value = self.cleaned_data.get("show_choices_flag")
        return "1" if value else "0"


# フォームセットの定義
TrnSurveyQuestionFormSet = inlineformset_factory(
    TrnSurvey,
    TrnSurveyQuestion,
    form=TrnSurveyQuestionForm,
    formset=CustomTrnSurveyQuestionFormSet,
    fields=["question", "show_choices_flag"],
    extra=0,
    can_delete=True,
)
