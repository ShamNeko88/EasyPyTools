from django.views import View
from django.views.generic import (
    TemplateView
)
from django.shortcuts import render
from django.http import JsonResponse
from .models import TrnSurvey, TrnSurveyQuestion
import uuid


# 初期ページ（アンケート作成）
class SurveyIndexView(View):
    template_name = "EasySurvey/survey-index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # フロントエンドから送信されたデータを取得
        title = request.POST.get('title')
        detail = request.POST.get('notes', '')  # 備考（オプション）
        questions = request.POST.getlist('questions[]')  # 質問リスト

        # バリデーション
        if not title or not questions:
            return JsonResponse({'error': 'タイトルと少なくとも1つの質問が必要です。'}, status=400)

        # TrnSurveyにデータを保存
        survey = TrnSurvey.objects.create(
            title=title,
            detail=detail,
            access_token=str(uuid.uuid4())  # アクセストークンを自動生成
        )

        # TrnSurveyQuestionにデータを保存
        for question_text in questions:
            if question_text.strip():  # 空の質問を無視
                TrnSurveyQuestion.objects.create(
                    survey_id=survey,
                    question=question_text.strip()
                )

        return JsonResponse({'message': 'アンケートが作成されました。', 'survey_id': survey.survey_id})


# アンケート回答ページ
class SurveyAnswerView(TemplateView):
    template_name = "EasySurvey/survey-answer.html"
