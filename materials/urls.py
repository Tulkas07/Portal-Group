from django.urls import path

from . import views

urlpatterns = [
    path('', views.material_list, name='material-list'),
    path('new/', views.MaterialCreate.as_view(), name='material-create'),
    path('<int:pk>/edit/', views.MaterialUpdate.as_view(), name='material-edit'),
    path('<int:pk>/delete/', views.MaterialDelete.as_view(), name='material-delete'),
]
