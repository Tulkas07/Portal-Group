from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


def _check_email_free(email, exclude_pk=None):
    email = email.strip().lower()
    taken = User.objects.filter(email__iexact=email)
    if exclude_pk:
        taken = taken.exclude(pk=exclude_pk)
    if taken.exists():
        raise forms.ValidationError("Користувач з такою поштою вже існує.")
    return email


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Ім'я", max_length=150)
    last_name = forms.CharField(label="Прізвище", max_length=150)
    email = forms.EmailField(label="Електронна пошта")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_email(self):
        return _check_email_free(self.cleaned_data["email"])


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label="Електронна пошта")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {"first_name": "Ім'я", "last_name": "Прізвище"}

    def clean_email(self):
        return _check_email_free(self.cleaned_data["email"], self.instance.pk)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "phone")
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}
