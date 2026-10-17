from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Vote(models.Model):
    title = models.CharField("Питання", max_length=200)
    description = models.TextField("Опис", blank=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Голосування"
        verbose_name_plural = "Голосування"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("vote-detail", args=[self.pk])


class Option(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name="options")
    text = models.CharField("Варіант", max_length=200)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text


class Ballot(models.Model):
    """Голос користувача. Один голос на голосування - переголосування замінює попередній."""
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name="ballots")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="ballots")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ballots")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["vote", "user"], name="unique_ballot_per_user")]

    def __str__(self):
        return f"{self.user}: {self.option}"
