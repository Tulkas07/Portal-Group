from django.urls import path

from forum import views

urlpatterns = [
    path('', views.topic_list, name="topic-list"),
    path('topic/new/', views.TopicCreate.as_view(), name="topic-create"),
    path('topic/<int:pk>/', views.topic_detail, name="topic-detail"),
    path('topic/<int:pk>/edit/', views.TopicUpdate.as_view(), name="topic-edit"),
    path('topic/<int:pk>/delete/', views.TopicDelete.as_view(), name="topic-delete"),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name="post-delete"),
    path('category/new/', views.CategoryCreate.as_view(), name="category-create"),
    path('category/<int:pk>/delete/', views.CategoryDelete.as_view(), name="category-delete"),
]
