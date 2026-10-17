from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    title = models.CharField("Назва", max_length=150)
    description = models.TextField("Опис", blank=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Опитування"
        verbose_name_plural = "Опитування"

    def __str__(self):
        return self.title


class Question(models.Model):
    CHOICE = "choice"
    TEXT = "text"
    KINDS = [(CHOICE, "Один варіант із списку"), (TEXT, "Текстова відповідь")]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    page = models.PositiveSmallIntegerField("Сторінка (крок)", default=1)
    text = models.CharField("Питання", max_length=250)
    kind = models.CharField("Тип", max_length=10, choices=KINDS, default=CHOICE)
    required = models.BooleanField("Обов'язкове", default=True)

    class Meta:
        ordering = ["page", "id"]

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField("Варіант", max_length=200)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text


class Submission(models.Model):
    """Пройдене опитування. Одне на користувача - повторне проходження замінює старі відповіді."""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["survey", "user"], name="unique_submission_per_user")]

    def __str__(self):
        return f"{self.user} - {self.survey}"


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True, related_name="answers")
    text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.question}: {self.choice or self.text}"
