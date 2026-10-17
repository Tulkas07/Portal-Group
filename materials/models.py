import os
import re

from django.contrib.auth.models import User
from django.db import models

IMAGES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
VIDEOS = {".mp4", ".webm", ".ogv"}
AUDIO = {".mp3", ".wav", ".ogg", ".m4a"}

YOUTUBE_RE = re.compile(r"(?:youtu\.be/|youtube\.com/(?:watch\?(?:\S*&)?v=|embed/|shorts/|live/))([\w-]{11})")


class Material(models.Model):
    title = models.CharField("Назва", max_length=150)
    description = models.TextField("Опис", blank=True)
    file = models.FileField("Файл", upload_to="materials/", blank=True)
    url = models.URLField("Посилання (у т.ч. YouTube)", blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="materials")
    created_at = models.DateTimeField("Додано", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"

    def __str__(self):
        return self.title

    @property
    def youtube_id(self):
        match = YOUTUBE_RE.search(self.url or "")
        return match.group(1) if match else ""

    @property
    def file_name(self):
        return os.path.basename(self.file.name) if self.file else ""

    @property
    def file_kind(self):
        """image / video / audio / pdf / other - від цього залежить, як файл показується на сторінці."""
        if not self.file:
            return ""
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in IMAGES:
            return "image"
        if ext in VIDEOS:
            return "video"
        if ext in AUDIO:
            return "audio"
        if ext == ".pdf":
            return "pdf"
        return "other"

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        return super().delete(*args, **kwargs)
