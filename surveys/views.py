from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Question, Choice, SurveyResult, Answer
# Create your views here.




def survey_list(request):
    surveys = Survey.objects.all()

    return render(
        request,
        "surveys/survey_list.html",
        {"surveys": surveys}
    )

def survey_start(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    questions = survey.questions.order_by("order")

    if not questions:
        return redirect("survey_list")

    request.session["survey_id"] = survey.id
    request.session["survey_answers"] = {}

    return redirect(
        "survey_question",
        survey_id=survey.id,
        question_id=questions.first().id
    )

def survey_question(request, survey_id, question_id):
    survey = get_object_or_404(Survey, id=survey_id)

    question = get_object_or_404(
        Question,
        id=question_id,
        survey=survey
    )

    questions = list(
        survey.questions.order_by("order")
    )

    current_index = questions.index(question)

    if request.method == "POST":
        choice_id = request.POST.get("choice")

        if choice_id:
            answers = request.session.get(
                "survey_answers",
                {}
            )

            answers[str(question.id)] = int(choice_id)

            request.session["survey_answers"] = answers

        
        if current_index + 1 < len(questions):
            next_question = questions[current_index + 1]

            return redirect(
                "survey_question",
                survey_id=survey.id,
                question_id=next_question.id
            )

        
        return redirect(
            "survey_finish",
            survey_id=survey.id
        )

    return render(
        request,
        "surveys/survey_question.html",
        {
            "survey": survey,
            "question": question,
            "current": current_index + 1,
            "total": len(questions),
        }
    )

def survey_finish(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    answers = request.session.get(
        "survey_answers",
        {}
    )

    
    SurveyResult.objects.filter(
        user=request.user,
        survey=survey
    ).delete()

    
    result = SurveyResult.objects.create(
        user=request.user,
        survey=survey
    )

    
    for question_id, choice_id in answers.items():

        question = Question.objects.get(
            id=question_id,
            survey=survey
        )

        choice = Choice.objects.get(
            id=choice_id,
            question=question
        )

        Answer.objects.create(
            result=result,
            question=question,
            choice=choice
        )

    
    request.session.pop("survey_id", None)
    request.session.pop("survey_answers", None)

    return render(
        request,
        "surveys/survey_finish.html",
        {"survey": survey}
    )