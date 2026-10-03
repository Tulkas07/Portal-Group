import calendar
from datetime import date
from django.shortcuts import render
from .models import Event
import calendar
from datetime import date
from django.shortcuts import render
from .models import Event


def event_list(request):
    events = Event.objects.order_by('date', 'time')

    return render(request, 'events/event_list.html', {
        'events': events
    })


def calendar_view(request):
    today = date.today()

    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    cal = calendar.monthcalendar(year, month)

    events = Event.objects.filter(
        date__year=year,
        date__month=month
    )

    events_by_day = {}

    for event in events:
        events_by_day.setdefault(event.date.day, []).append(event)

    calendar_days = []

    for week in cal:
        week_data = []

        for day in week:
            week_data.append({
                'day': day,
                'events': events_by_day.get(day, [])
            })

        calendar_days.append(week_data)

    # Предыдущий месяц
    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    # Следующий месяц
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    return render(request, 'calendar.html', {
        'calendar': calendar_days,
        'year': year,
        'month': month,

        'previous_year': previous_year,
        'previous_month': previous_month,

        'next_year': next_year,
        'next_month': next_month,
    })