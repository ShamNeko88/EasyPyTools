from django.views import View
from django.views.generic import (
    TemplateView
)
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import TrnSurvey, TrnSurveyQuestion, TrnSurveyAnswer
import uuid
from django.utils import timezone


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
class SurveyAnswerView(View):
    template_name = "EasySurvey/survey-answer.html"

    def get(self, request, *args, **kwargs):
        # アクセストークンを使ってアンケートを取得
        access_token = kwargs.get('access_token')
        survey = get_object_or_404(TrnSurvey, access_token=access_token)
        questions = TrnSurveyQuestion.objects.filter(survey_id=survey)

        context = {
            'survey': survey,
            'questions': questions,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        access_token = kwargs.get('access_token')
        survey = get_object_or_404(TrnSurvey, access_token=access_token)
        questions = TrnSurveyQuestion.objects.filter(survey_id=survey)

        responder_name = request.POST.get('responder')
        if not responder_name:
            return JsonResponse({'error': '回答者名は必須です。'}, status=400)

        for question in questions:
            answer_text = request.POST.get(f'question_{question.question_id}')
            if answer_text:
                # データを更新または作成
                TrnSurveyAnswer.objects.update_or_create(
                    survey_id=survey,
                    question_id=question,
                    responder=responder_name,
                    defaults={
                        'answer': answer_text,
                        'updated_at': timezone.now(),  # 更新日時を更新
                    }
                )

        return JsonResponse({'message': '回答が保存されました。'})
