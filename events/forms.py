from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "description", "date", "time")
        labels = {"title": "Назва", "description": "Опис", "date": "Дата", "time": "Час (необов'язково)"}
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "time": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
        }
