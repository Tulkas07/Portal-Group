from django.urls import path

from grades import views

urlpatterns = [
    path('', views.diary_list, name="diary-list"),
    path('grade/new/', views.GradeCreate.as_view(), name="grade-create"),
    path('grade/<int:pk>/edit/', views.GradeUpdate.as_view(), name="grade-edit"),
    path('grade/<int:pk>/delete/', views.GradeDelete.as_view(), name="grade-delete"),
    path('student/new/', views.StudentCreate.as_view(), name="student-create"),
    path('subject/new/', views.SubjectCreate.as_view(), name="subject-create"),
]
