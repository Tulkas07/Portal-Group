from django.urls import path

from . import views

urlpatterns = [
    path('', views.survey_list, name='survey-list'),
    path('new/', views.SurveyCreate.as_view(), name='survey-create'),
    path('<int:pk>/take/', views.survey_take, {'step': 1}, name='survey-take'),
    path('<int:pk>/take/<int:step>/', views.survey_take, name='survey-take'),
    path('<int:pk>/results/', views.survey_results, name='survey-results'),
    path('<int:pk>/edit/', views.SurveyUpdate.as_view(), name='survey-edit'),
    path('<int:pk>/delete/', views.SurveyDelete.as_view(), name='survey-delete'),
    path('<int:pk>/questions/', views.survey_questions, name='survey-questions'),
    path('<int:pk>/questions/new/', views.QuestionCreate.as_view(), name='question-create'),
    path('question/<int:pk>/edit/', views.QuestionUpdate.as_view(), name='question-edit'),
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
]
