from django import forms

from core.generic import split_lines, sync_children

from .models import Question


class QuestionForm(forms.ModelForm):
    page = forms.IntegerField(label="Сторінка (крок)", min_value=1, max_value=50, initial=1,
                              help_text="Питання з однаковим номером показуються разом на одній сторінці.")
    choices_text = forms.CharField(label="Варіанти відповіді (кожен з нового рядка)", required=False,
                                   widget=forms.Textarea(attrs={"rows": 5}))

    class Meta:
        model = Question
        fields = ("page", "text", "kind", "required")
        labels = {"text": "Питання", "kind": "Тип питання", "required": "Обов'язкове питання"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["choices_text"].initial = "\n".join(c.text for c in self.instance.choices.all())

    def clean(self):
        data = super().clean()
        lines = split_lines(data.get("choices_text", ""))
        if data.get("kind") == Question.CHOICE:
            if not 2 <= len(lines) <= 10:
                self.add_error("choices_text", "Для питання з варіантами потрібно від 2 до 10 варіантів.")
            elif len({line.lower() for line in lines}) != len(lines):
                self.add_error("choices_text", "Варіанти не повинні повторюватися.")
            elif any(len(line) > 200 for line in lines):
                self.add_error("choices_text", "Варіант не може бути довшим за 200 символів.")
        return data

    def save(self, commit=True):
        question = super().save(commit)
        lines = split_lines(self.cleaned_data["choices_text"]) if question.kind == Question.CHOICE else []
        sync_children(question.choices, lines)
        return question


class PageForm(forms.Form):
    """Форма однієї сторінки опитування - поля будуються з її питань."""

    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for q in questions:
            if q.kind == Question.CHOICE:
                field = forms.ChoiceField(label=q.text, required=q.required, widget=forms.RadioSelect,
                                          choices=[(c.pk, c.text) for c in q.choices.all()])
            else:
                field = forms.CharField(label=q.text, required=q.required, max_length=1000,
                                        widget=forms.Textarea(attrs={"rows": 3}))
            self.fields[f"q{q.pk}"] = field
