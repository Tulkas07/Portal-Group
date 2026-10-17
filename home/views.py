from django.shortcuts import render
from django.utils import timezone

from announcements.models import Announcement
from events.models import Event
from forum.models import Topic
from materials.models import Material
from surveys.models import Survey
from votes.models import Vote


def home(request):
    """Головна: інформація про групу та віджети інших розділів."""
    return render(request, "home/home.html", {
        "announcements": Announcement.objects.all()[:3],
        "events": Event.objects.filter(date__gte=timezone.localdate()).order_by("date", "time")[:4],
        "topics": Topic.objects.select_related("author", "category").order_by("-created_at")[:4],
        "votes": Vote.objects.all()[:3],
        "surveys": Survey.objects.all()[:3],
        "materials": Material.objects.all()[:3],
    })
