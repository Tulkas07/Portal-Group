from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.permissions import role_name

from .forms import ProfileForm, RegisterForm, UserEditForm
from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Реєстрація успішна. Ласкаво просимо!")
        return redirect("home")
    return render(request, "users/register.html", {"form": form})


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    is_post = request.method == "POST"
    user_form = UserEditForm(request.POST if is_post else None, instance=request.user)
    profile_form = ProfileForm(request.POST if is_post else None, instance=profile)
    if is_post and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Профіль оновлено.")
        return redirect("profile")
    return render(request, "users/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "role": role_name(request.user),
    })
