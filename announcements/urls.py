from django.urls import path

from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement-list'),
    path('new/', views.AnnouncementCreate.as_view(), name='announcement-create'),
    path('<int:pk>/edit/', views.AnnouncementUpdate.as_view(), name='announcement-edit'),
    path('<int:pk>/delete/', views.AnnouncementDelete.as_view(), name='announcement-delete'),
]
