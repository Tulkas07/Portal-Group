from django import forms

from .models import Grade, Student, Subject


class GradeForm(forms.ModelForm):
    grade = forms.IntegerField(label="Оцінка (1-12)", min_value=1, max_value=12)

    class Meta:
        model = Grade
        fields = ("student", "subject", "grade")
        labels = {"student": "Учень", "subject": "Предмет"}


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("user", "group")
        labels = {"user": "Користувач", "group": "Група"}


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("subject",)
        labels = {"subject": "Назва предмета"}
