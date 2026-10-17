"""URL configuration for core project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('users.urls')),
    path('forum/', include('forum.urls')),
    path('events/', include('events.urls')),
    path('diary/', include('grades.urls')),
    path('announcements/', include('announcements.urls')),
    path('votes/', include('votes.urls')),
    path('surveys/', include('surveys.urls')),
    path('materials/', include('materials.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
