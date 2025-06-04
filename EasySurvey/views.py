from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import TrnSurvey, TrnSurveyQuestion, TrnSurveyAnswer
import uuid
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.views.generic import DeleteView, TemplateView
from django.urls import reverse_lazy
from .forms import TrnSurveyForm, TrnSurveyQuestionFormSet


# 初期ページ（アンケート作成）
class SurveyIndexView(View):
    template_name = "EasySurvey/survey-index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        detail = request.POST.get("notes", "")
        questions = request.POST.getlist("questions[]")
        show_choices = request.POST.getlist("show_choices[]")  # 選択肢の有無

        # デバッグ出力
        print("質問数:", len(questions))
        print("show_choices:", show_choices)
        print("POST データ全体:", request.POST)

        # バリデーション
        if not title or not questions:
            return render(request, self.template_name, 
                         {"error": "タイトルと少なくとも1つの質問が必要です。"})

        created_by = request.user if not isinstance(request.user, AnonymousUser) else None

        # TrnSurveyにデータを保存
        survey = TrnSurvey.objects.create(
            title=title,
            detail=detail,
            access_token=str(uuid.uuid4()),
            created_by=created_by,
        )

        # TrnSurveyQuestionにデータを保存
        for i, question_text in enumerate(questions):
            if question_text.strip():
                show_choices_flag = "1" if str(i+1) in show_choices else "0"
                TrnSurveyQuestion.objects.create(
                    survey_id=survey,
                    question=question_text.strip(),
                    show_choices_flag=show_choices_flag  # フラグを設定
                )

        return redirect(reverse("survey-complete", 
                              kwargs={"access_token": survey.access_token}))


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

        # 回答者名の重複チェック
        if TrnSurveyAnswer.objects.filter(survey_id=survey, responder=responder_name).exists():
            return JsonResponse(
                {"error": "この名前は既に使用されています。別の名前を入力してください。"}, 
                status=400
            )

        # 各質問に対する回答とコメントを取得
        for question in questions:
            answer_text = request.POST.get(f"question_{question.question_id}")
            comment_text = request.POST.get(f"comment_{question.question_id}", "")
            if answer_text or comment_text:
                if not answer_text:
                    answer_text = "0"
                TrnSurveyAnswer.objects.create(
                    survey_id=survey,
                    question_id=question,
                    responder=responder_name,
                    answer=answer_text,
                    comment=comment_text,
                )

        # 成功時のレスポンス
        return JsonResponse({
            "success": True,
            "redirect_url": reverse("survey-result", kwargs={"access_token": access_token})
        })


# アンケート結果ページ
class SurveyResultView(View):
    template_name = "EasySurvey/survey-result.html"

    def get(self, request, *args, **kwargs):
        # アクセストークンを使ってアンケートを取得
        access_token = kwargs.get("access_token")
        survey = get_object_or_404(TrnSurvey, access_token=access_token)
        questions = TrnSurveyQuestion.objects.filter(survey_id=survey).order_by('question_id')

        # 回答者一覧を取得
        responders = TrnSurveyAnswer.objects.filter(
            survey_id=survey
        ).values_list('responder', flat=True).distinct().order_by('responder')

        # 各質問に対する回答の集計
        results = []
        for question in questions:
            # 各回答者の回答を取得（回答がない場合はNone）
            answers = []
            for responder in responders:
                answer = TrnSurveyAnswer.objects.filter(
                    survey_id=survey,
                    question_id=question,
                    responder=responder
                ).first()
                answers.append(answer)
            
            results.append({
                "question": question.question,
                "answers": answers,
            })

        context = {
            "survey": survey,
            "results": results,
            "responders": responders,
        }
        return render(request, self.template_name, context)


# アンケート一覧ページ
class SurveyListView(LoginRequiredMixin, View):
    template_name = "EasySurvey/survey-list.html"

    def get(self, request, *args, **kwargs):
        # ログインしているユーザーが作成したアンケートを取得
        created_surveys = TrnSurvey.objects.filter(created_by=request.user)

        context = {
            "created_surveys": created_surveys,
        }
        return render(request, self.template_name, context)


# アンケート完了ページ
class SurveyCompleteView(View):
    template_name = "EasySurvey/survey-complete.html"

    def get(self, request, *args, **kwargs):
        access_token = kwargs.get("access_token")
        survey_url = request.build_absolute_uri(
            reverse("survey-answer", kwargs={"access_token": access_token})
        )
        return render(request, self.template_name, {"survey_url": survey_url})


# アンケート削除ページ
class SurveyDeleteView(LoginRequiredMixin, DeleteView):
    model = TrnSurvey
    template_name = "EasySurvey/survey-delete.html"
    success_url = reverse_lazy("survey-list")

    def get_queryset(self):
        # ログインユーザーが作成したアンケートのみ削除可能
        return self.model.objects.filter(created_by=self.request.user)

    # 削除ページで削除するデータを使いたい
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["survey"] = self.get_object()
        return context


# 質問削除ページ
class QuestionDeleteView(DeleteView):
    model = TrnSurveyQuestion
    template_name = "EasySurvey/survey-question-delete.html"

    def get_success_url(self):
        # 削除後にアンケート編集画面に遷移
        survey_id = self.object.survey_id.survey_id  # 質問に関連するアンケートIDを取得
        return reverse_lazy("survey-edit", kwargs={"pk": survey_id})

    def get_queryset(self):
        # ログインユーザーが作成した質問のみ削除可能
        return self.model.objects.filter(survey_id__created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.get_object()
        return context


# アンケート編集ページ
class SurveyEditView(LoginRequiredMixin, View):
    template_name = "EasySurvey/survey-edit.html"

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(TrnSurvey, pk=kwargs["pk"])
        survey_form = TrnSurveyForm(instance=survey)
        question_formset = TrnSurveyQuestionFormSet(instance=survey)
        # 回答者一覧を取得
        answerers = TrnSurveyAnswer.objects.filter(question_id__survey_id=survey).values_list('responder', flat=True).distinct()
        return render(
            request,
            self.template_name,
            {
                "survey_form": survey_form,
                "question_formset": question_formset,
                "answerers": answerers,  # 回答者一覧をコンテキストに追加
            },
        )

    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(TrnSurvey, pk=kwargs["pk"])
        survey_form = TrnSurveyForm(request.POST, instance=survey)
        question_formset = TrnSurveyQuestionFormSet(request.POST, instance=survey)

        # デバッグ: POSTデータを確認
        print(request.POST)
        # 新規追加された質問を取得
        new_questions = request.POST.getlist("new_questions[]")
        new_show_choices_flags = request.POST.getlist("new_show_choices_flag[]")
        print("New Questions:", new_questions)
        if survey_form.is_valid() and question_formset.is_valid():
            survey_form.save()
            question_formset.save()

            # 新規追加された質問を保存
            for i, question_text in enumerate(new_questions):
                if question_text.strip():
                    show_choices_flag = "1" if (i < len(new_show_choices_flags)) else "0"
                    TrnSurveyQuestion.objects.create(
                        survey_id=survey,
                        question=question_text.strip(),
                        show_choices_flag=show_choices_flag
                    )

            return redirect(
                reverse_lazy(
                    "survey-result", kwargs={"access_token": survey.access_token}
                )
            )

        return render(
            request,
            self.template_name,
            {
                "survey_form": survey_form,
                "question_formset": question_formset,
            },
        )


# アンケート回答者削除ページ
class ResponderDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "EasySurvey/survey-responder-delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = get_object_or_404(TrnSurvey, pk=self.kwargs["pk"])
        context["survey"] = survey
        return context

    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(TrnSurvey, pk=self.kwargs["pk"])
        TrnSurveyAnswer.objects.filter(survey_id=survey).delete()
        return redirect(reverse_lazy("survey-edit", kwargs={"pk": survey.pk}))


# 回答編集ビュー
class SurveyAnswerEditView(View):
    template_name = "EasySurvey/survey-answer-edit.html"

    def get(self, request, *args, **kwargs):
        access_token = kwargs.get("access_token")
        answer_id = kwargs.get("answer_id")
        
        # アンケートと回答を取得
        survey = get_object_or_404(TrnSurvey, access_token=access_token)
        answer = get_object_or_404(TrnSurveyAnswer, answer_id=answer_id)
        questions = TrnSurveyQuestion.objects.filter(survey_id=survey)

        context = {
            "survey": survey,
            "answer": answer,
            "questions": questions,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        access_token = kwargs.get("access_token")
        answer_id = kwargs.get("answer_id")
        
        # アンケートと回答を取得
        survey = get_object_or_404(TrnSurvey, access_token=access_token)
        answer = get_object_or_404(TrnSurveyAnswer, answer_id=answer_id)
        questions = TrnSurveyQuestion.objects.filter(survey_id=survey)

        # 回答の更新
        for question in questions:
            answer_text = request.POST.get(f"question_{question.question_id}")
            comment_text = request.POST.get(f"comment_{question.question_id}", "")
            
            if answer_text or comment_text:
                if not answer_text:
                    answer_text = "0"
                TrnSurveyAnswer.objects.update_or_create(
                    survey_id=survey,
                    question_id=question,
                    responder=answer.responder,
                    defaults={
                        "answer": answer_text,
                        "comment": comment_text,
                        "updated_at": timezone.now(),
                    },
                )

        # 更新後に結果ページへリダイレクト
        return redirect("survey-result", access_token=access_token)
