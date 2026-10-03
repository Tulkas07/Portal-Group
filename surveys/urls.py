from django.urls import path
from . import views


urlpatterns = [
    path("",views.survey_list,name="survey_list"),
    path("<int:survey_id>/start/",views.survey_start,name="survey_start"),
    path("<int:survey_id>/question/<int:question_id>/",views.survey_question,name="survey_question"),
    path("<int:survey_id>/finish/",views.survey_finish,name="survey_finish"),
]