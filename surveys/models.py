from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    text = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.text


class SurveyResult(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="results"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="survey_results"
    )
    completed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} — {self.survey}"


class Answer(models.Model):
    result = models.ForeignKey(
        SurveyResult,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.question} → {self.choice}"