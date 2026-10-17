import calendar

from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView

from core.generic import DeletePage, FormPage
from core.permissions import ManagerRequiredMixin

from .forms import EventForm
from .models import Event

MONTHS = ["січень", "лютий", "березень", "квітень", "травень", "червень",
          "липень", "серпень", "вересень", "жовтень", "листопад", "грудень"]


def event_list(request):
    events = Event.objects.order_by("date", "time")
    return render(request, "events/event_list.html", {"events": events, "today": timezone.localdate()})


def calendar_view(request):
    today = timezone.localdate()
    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
        if not (1 <= month <= 12 and 1900 <= year <= 2100):
            raise ValueError
    except ValueError:
        year, month = today.year, today.month

    events_by_day = {}
    for event in Event.objects.filter(date__year=year, date__month=month).order_by("time"):
        events_by_day.setdefault(event.date.day, []).append(event)

    weeks = [
        [{"day": day, "events": events_by_day.get(day, []),
          "is_today": (year, month, day) == (today.year, today.month, today.day)} for day in week]
        for week in calendar.monthcalendar(year, month)
    ]

    previous_year, previous_month = (year - 1, 12) if month == 1 else (year, month - 1)
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

    return render(request, "events/calendar.html", {
        "calendar": weeks, "year": year, "month": month, "month_name": MONTHS[month - 1],
        "previous_year": previous_year, "previous_month": previous_month,
        "next_year": next_year, "next_month": next_month,
    })


class EventCreate(ManagerRequiredMixin, FormPage, CreateView):
    model = Event
    form_class = EventForm
    page_title = "Нова подія"
    success_url = reverse_lazy("event_list")


class EventUpdate(ManagerRequiredMixin, FormPage, UpdateView):
    model = Event
    form_class = EventForm
    page_title = "Редагування події"
    delete_url_name = "event_delete"
    success_url = reverse_lazy("event_list")


class EventDelete(ManagerRequiredMixin, DeletePage, DeleteView):
    model = Event
    success_url = reverse_lazy("event_list")
