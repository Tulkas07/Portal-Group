from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from core.generic import DeletePage, FormPage
from core.permissions import ManagerRequiredMixin, can_manage
from .forms import PageForm, QuestionForm
from .models import Answer, Choice, Question, Submission, Survey


def survey_list(request):
    surveys = Survey.objects.annotate(n_questions=Count("questions", distinct=True),
                                      n_submissions=Count("submissions", distinct=True))
    done = set()
    if request.user.is_authenticated:
        done = set(Submission.objects.filter(user=request.user).values_list("survey_id", flat=True))
    return render(request, "surveys/survey_list.html", {"surveys": surveys, "done": done})



@login_required
def survey_take(request, pk, step=1):
    survey = get_object_or_404(Survey, pk=pk)
    pages = list(survey.questions.order_by("page").values_list("page", flat=True).distinct())
    if not pages:
        messages.info(request, "У цьому опитуванні поки немає питань.")
        return redirect("survey-list")
    if not 1 <= step <= len(pages):
        raise Http404

    key = f"survey_{pk}"
    state = request.session.get(key, {"done": 0, "answers": {}})
    if step > state["done"] + 1:  
        return redirect("survey-take", pk=pk, step=state["done"] + 1)

    questions = list(survey.questions.filter(page=pages[step - 1]).prefetch_related("choices"))
    initial = {f"q{q.pk}": state["answers"].get(str(q.pk)) for q in questions}
    is_post = request.method == "POST"
    form = PageForm(questions, request.POST if is_post else None, initial=initial)

    if is_post and form.is_valid():
        for q in questions:
            state["answers"][str(q.pk)] = form.cleaned_data[f"q{q.pk}"]
        state["done"] = max(state["done"], step)
        request.session[key] = state
        if step < len(pages):
            return redirect("survey-take", pk=pk, step=step + 1)
        _save_submission(request, survey, state["answers"])
        request.session.pop(key, None)
        messages.success(request, "Дякуємо! Ваші відповіді збережено.")
        return redirect("survey-list")

    return render(request, "surveys/survey_take.html", {
        "survey": survey, "form": form, "step": step, "total_steps": len(pages),
        "is_last": step == len(pages), "prev_step": step - 1 if step > 1 else None,
    })


def _save_submission(request, survey, answers):
    questions = {str(q.pk): q for q in survey.questions.all()}
    with transaction.atomic():
        Submission.objects.filter(survey=survey, user=request.user).delete()
        submission = Submission.objects.create(survey=survey, user=request.user)
        for qid, value in answers.items():
            question = questions.get(qid)
            if question is None or value in ("", None):
                continue
            if question.kind == Question.CHOICE:
                choice = Choice.objects.filter(pk=value, question=question).first()
                if choice:
                    Answer.objects.create(submission=submission, question=question, choice=choice)
            else:
                Answer.objects.create(submission=submission, question=question, text=value)




@login_required
def survey_results(request, pk):
    if not can_manage(request.user):
        raise PermissionDenied
    survey = get_object_or_404(Survey, pk=pk)
    total = survey.submissions.count()
    questions = list(survey.questions.prefetch_related("choices"))
    for q in questions:
        if q.kind == Question.CHOICE:
            rows = list(q.choices.annotate(n=Count("answers")))
            answered = sum(r.n for r in rows)
            for r in rows:
                r.percent = round(r.n * 100 / answered) if answered else 0
            q.rows, q.answered = rows, answered
        else:
            q.text_answers = list(q.answers.exclude(text="").select_related("submission__user"))
    submissions = survey.submissions.select_related("user").order_by("-created_at")
    return render(request, "surveys/survey_results.html", {
        "survey": survey, "questions": questions, "total": total, "submissions": submissions,
    })



class SurveyCreate(ManagerRequiredMixin, FormPage, CreateView):
    model = Survey
    fields = ("title", "description")
    page_title = "Нове опитування"

    def get_success_url(self):
        return reverse("survey-questions", args=[self.object.pk])


class SurveyUpdate(ManagerRequiredMixin, FormPage, UpdateView):
    model = Survey
    fields = ("title", "description")
    page_title = "Редагування опитування"
    delete_url_name = "survey-delete"
    success_url = reverse_lazy("survey-list")


class SurveyDelete(ManagerRequiredMixin, DeletePage, DeleteView):
    model = Survey
    success_url = reverse_lazy("survey-list")


@login_required
def survey_questions(request, pk):
    if not can_manage(request.user):
        raise PermissionDenied
    survey = get_object_or_404(Survey, pk=pk)
    questions = survey.questions.prefetch_related("choices")
    return render(request, "surveys/survey_questions.html", {"survey": survey, "questions": questions})


class QuestionCreate(ManagerRequiredMixin, FormPage, CreateView):
    model = Question
    form_class = QuestionForm
    page_title = "Нове питання"

    def form_valid(self, form):
        form.instance.survey = get_object_or_404(Survey, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("survey-questions", args=[self.object.survey_id])


class QuestionUpdate(ManagerRequiredMixin, FormPage, UpdateView):
    model = Question
    form_class = QuestionForm
    page_title = "Редагування питання"
    delete_url_name = "question-delete"

    def get_success_url(self):
        return reverse("survey-questions", args=[self.object.survey_id])


class QuestionDelete(ManagerRequiredMixin, DeletePage, DeleteView):
    model = Question

    def get_success_url(self):
        return reverse("survey-questions", args=[self.object.survey_id])
