from django.urls import path

from . import views

urlpatterns = [
    path('', views.vote_list, name='vote-list'),
    path('new/', views.VoteCreate.as_view(), name='vote-create'),
    path('<int:pk>/', views.vote_detail, name='vote-detail'),
    path('<int:pk>/edit/', views.VoteUpdate.as_view(), name='vote-edit'),
    path('<int:pk>/delete/', views.VoteDelete.as_view(), name='vote-delete'),
]
