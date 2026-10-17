from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from users import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password/', PasswordChangeView.as_view(
        template_name='form.html',
        success_url=reverse_lazy('profile'),
        extra_context={'title': 'Зміна пароля'},
    ), name='password'),
]
