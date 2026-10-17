from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.generic import DeletePage, FormPage
from core.permissions import ManagerRequiredMixin

from .forms import MaterialForm
from .models import Material


def material_list(request):
    return render(request, "materials/material_list.html", {"materials": Material.objects.all()})


class MaterialCreate(ManagerRequiredMixin, FormPage, CreateView):
    model = Material
    form_class = MaterialForm
    page_title = "Новий матеріал"
    success_url = reverse_lazy("material-list")

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class MaterialUpdate(ManagerRequiredMixin, FormPage, UpdateView):
    model = Material
    form_class = MaterialForm
    page_title = "Редагування матеріалу"
    delete_url_name = "material-delete"
    success_url = reverse_lazy("material-list")


class MaterialDelete(ManagerRequiredMixin, DeletePage, DeleteView):
    model = Material
    success_url = reverse_lazy("material-list")
