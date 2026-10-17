from django.contrib import admin

from .models import Ballot, Option, Vote

admin.site.register(Vote)
admin.site.register(Option)
admin.site.register(Ballot)
