from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import TrnSurvey, TrnSurveyQuestion, TrnSurveyAnswer
import uuid
from django.utils import timezone
from django.db.models import Count


# 初期ページ（アンケート作成）
class SurveyIndexView(View):
    template_name = "EasySurvey/survey-index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # フロントエンドから送信されたデータを取得
        title = request.POST.get("title")
        detail = request.POST.get("notes", "")  # 備考（オプション）
        questions = request.POST.getlist("questions[]")  # 質問リスト

        # バリデーション
        if not title or not questions:
            return JsonResponse(
                {"error": "タイトルと少なくとも1つの質問が必要です。"}, status=400
            )

        # TrnSurveyにデータを保存
        survey = TrnSurvey.objects.create(
            title=title,
            detail=detail,
            access_token=str(uuid.uuid4()),  # アクセストークンを自動生成
        )

        # TrnSurveyQuestionにデータを保存
        for question_text in questions:
            if question_text.strip():  # 空の質問を無視
                TrnSurveyQuestion.objects.create(
                    survey_id=survey, question=question_text.strip()
                )

        return JsonResponse(
            {"message": "アンケートが作成されました。", "survey_id": survey.survey_id}
        )


# アンケート回答ページ
class SurveyAnswerView(View):
    template_name = "EasySurvey/survey-answer.html"

    def get(self, request, *args, **kwargs):
        # アクセストークンを使ってアンケートを取得
        access_token = kwargs.get("access_token")
        survey = get_object_or_404(TrnSurvey, access_token=access_token)
        questions = TrnSurveyQuestion.objects.filter(survey_id=survey)

        context = {"survey": survey, "questions": questions}
        return render(request, self.template_name, context)

    # POSTメソッドで回答を保存
    def post(self, request, *args, **kwargs):
        access_token = kwargs.get("access_token")
        survey = get_object_or_404(TrnSurvey, access_token=access_token)
        questions = TrnSurveyQuestion.objects.filter(survey_id=survey)

        # フロントエンドから送信されたデータを取得
        responder_name = request.POST.get("responder")  # 回答者名
        # バリデーション
        if not responder_name:
            return JsonResponse({"error": "回答者名は必須です。"}, status=400)

        # 各質問に対する回答とコメントを取得
        for question in questions:
            answer_text = request.POST.get(
                f"question_{question.question_id}"
            )  # 回答を取得
            comment_text = request.POST.get(
                f"comment_{question.question_id}", ""
            )  # コメントを取得
            if answer_text:
                # データを更新または作成
                TrnSurveyAnswer.objects.update_or_create(
                    survey_id=survey,
                    question_id=question,
                    responder=responder_name,
                    defaults={
                        "answer": answer_text,
                        "comment": comment_text,  # コメントを保存
                        "updated_at": timezone.now(),  # 更新日時を更新
                    },
                )

        # 回答保存後に結果ページへリダイレクト
        return redirect("survey_result", access_token=access_token)


# アンケート結果ページ
class SurveyResultView(View):
    template_name = "EasySurvey/survey-result.html"

    def get(self, request, *args, **kwargs):
        # アクセストークンを使ってアンケートを取得
        access_token = kwargs.get("access_token")
        survey = get_object_or_404(TrnSurvey, access_token=access_token)
        questions = TrnSurveyQuestion.objects.filter(survey_id=survey)

        # 各質問に対する回答の集計
        results = []
        for question in questions:
            answers = TrnSurveyAnswer.objects.filter(question_id=question)
            results.append(
                {
                    "question": question.question,
                    "answers": answers,  # 各回答者の回答を含む
                }
            )

        context = {
            "survey": survey,
            "results": results,
        }
        return render(request, self.template_name, context)
