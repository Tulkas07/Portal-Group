from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.generic import DeletePage, FormPage
from core.permissions import AdminRequiredMixin

from .forms import GradeForm, StudentForm, SubjectForm
from .models import Grade, Student, Subject


@login_required
def diary_list(request):
    """Таблиця: рядки - учні, стовпці - предмети, у клітинках - оцінки."""
    students = Student.objects.select_related("user").order_by("group", "user__last_name", "user__username")
    subjects = list(Subject.objects.order_by("subject"))

    cells = defaultdict(list)
    for grade in Grade.objects.order_by("id"):
        cells[(grade.student_id, grade.subject_id)].append(grade)

    rows = []
    for student in students:
        row_cells = [cells[(student.id, subject.id)] for subject in subjects]
        values = [g.grade for cell in row_cells for g in cell]
        rows.append({
            "student": student,
            "cells": [{"subject": s, "grades": c} for s, c in zip(subjects, row_cells)],
            "average": round(sum(values) / len(values), 1) if values else None,
        })
    return render(request, "grades/diary_list.html", {"rows": rows, "subjects": subjects})


class GradeCreate(AdminRequiredMixin, FormPage, CreateView):
    model = Grade
    form_class = GradeForm
    page_title = "Нова оцінка"
    success_url = reverse_lazy("diary-list")

    def get_initial(self):
        # посилання «+» у таблиці підставляє учня та предмет
        return {"student": self.request.GET.get("student"), "subject": self.request.GET.get("subject")}


class GradeUpdate(AdminRequiredMixin, FormPage, UpdateView):
    model = Grade
    form_class = GradeForm
    page_title = "Редагування оцінки"
    delete_url_name = "grade-delete"
    success_url = reverse_lazy("diary-list")


class GradeDelete(AdminRequiredMixin, DeletePage, DeleteView):
    model = Grade
    success_url = reverse_lazy("diary-list")


class StudentCreate(AdminRequiredMixin, FormPage, CreateView):
    model = Student
    form_class = StudentForm
    page_title = "Новий учень"
    success_url = reverse_lazy("diary-list")


class SubjectCreate(AdminRequiredMixin, FormPage, CreateView):
    model = Subject
    form_class = SubjectForm
    page_title = "Новий предмет"
    success_url = reverse_lazy("diary-list")
