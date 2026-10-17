from django import forms

from core.generic import split_lines, sync_children

from .models import Option, Vote


class BallotForm(forms.Form):
    option = forms.ModelChoiceField(queryset=Option.objects.none(), widget=forms.RadioSelect,
                                    empty_label=None, label="", error_messages={"required": "Оберіть варіант."})

    def __init__(self, vote, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["option"].queryset = vote.options.all()  # чужі варіанти не пройдуть валідацію


class VoteForm(forms.ModelForm):
    options_text = forms.CharField(label="Варіанти відповіді (кожен з нового рядка)",
                                   widget=forms.Textarea(attrs={"rows": 5}))

    class Meta:
        model = Vote
        fields = ("title", "description")
        labels = {"title": "Питання", "description": "Опис (необов'язково)"}
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["options_text"].initial = "\n".join(o.text for o in self.instance.options.all())

    def clean_options_text(self):
        lines = split_lines(self.cleaned_data["options_text"])
        if not 2 <= len(lines) <= 10:
            raise forms.ValidationError("Потрібно від 2 до 10 варіантів.")
        if len({line.lower() for line in lines}) != len(lines):
            raise forms.ValidationError("Варіанти не повинні повторюватися.")
        if any(len(line) > 200 for line in lines):
            raise forms.ValidationError("Варіант не може бути довшим за 200 символів.")
        return "\n".join(lines)

    def save(self, commit=True):
        vote = super().save(commit)
        sync_children(vote.options, split_lines(self.cleaned_data["options_text"]))
        return vote
