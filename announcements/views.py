from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.generic import DeletePage, FormPage
from core.permissions import ManagerRequiredMixin

from .models import Announcement

FIELDS = ("title", "text")


def announcement_list(request):
    items = Announcement.objects.select_related("author")
    return render(request, "announcements/announcement_list.html", {"announcements": items})


class AnnouncementCreate(ManagerRequiredMixin, FormPage, CreateView):
    model = Announcement
    fields = FIELDS
    page_title = "Нове оголошення"
    success_url = reverse_lazy("announcement-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnnouncementUpdate(ManagerRequiredMixin, FormPage, UpdateView):
    model = Announcement
    fields = FIELDS
    page_title = "Редагування оголошення"
    delete_url_name = "announcement-delete"
    success_url = reverse_lazy("announcement-list")


class AnnouncementDelete(ManagerRequiredMixin, DeletePage, DeleteView):
    model = Announcement
    success_url = reverse_lazy("announcement-list")
