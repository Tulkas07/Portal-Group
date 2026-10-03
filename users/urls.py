from django.urls import path
from users import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
]