from django.urls import path

from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('new/', views.EventCreate.as_view(), name='event_create'),
    path('<int:pk>/edit/', views.EventUpdate.as_view(), name='event_edit'),
    path('<int:pk>/delete/', views.EventDelete.as_view(), name='event_delete'),
]
