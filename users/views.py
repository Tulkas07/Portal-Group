from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
