from django.contrib import admin

from .models import Answer, Choice, Question, Submission, Survey

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Answer)
