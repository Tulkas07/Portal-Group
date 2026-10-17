from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField("Про себе", blank=True, max_length=500)
    phone = models.CharField("Телефон", max_length=20, blank=True)

    def __str__(self):
        return f"Профіль {self.user}"
