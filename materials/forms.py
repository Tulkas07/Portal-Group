import os

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .models import Material

# файли, які браузер може виконати як код на нашому сайті, не приймаємо
BLOCKED = {".html", ".htm", ".xhtml", ".svg", ".js", ".php", ".exe", ".bat", ".sh"}


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ("title", "description", "file", "url")
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if isinstance(file, UploadedFile):  # перевіряємо лише новий файл
            if os.path.splitext(file.name)[1].lower() in BLOCKED:
                raise forms.ValidationError("Цей тип файлів завантажувати не можна.")
            if file.size > settings.MAX_UPLOAD_MB * 1024 * 1024:
                raise forms.ValidationError(f"Файл завеликий (максимум {settings.MAX_UPLOAD_MB} МБ).")
        return file

    def clean(self):
        data = super().clean()
        if not data.get("file") and not data.get("url"):
            raise forms.ValidationError("Додайте файл або посилання.")
        return data
