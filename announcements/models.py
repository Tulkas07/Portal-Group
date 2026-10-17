from django.contrib.auth.models import User
from django.db import models


class Announcement(models.Model):
    title = models.CharField("Заголовок", max_length=120)
    text = models.TextField("Текст")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="announcements")
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Оголошення"
        verbose_name_plural = "Оголошення"

    def __str__(self):
        return self.title
