from django.shortcuts import render
from .models import Grade
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
# Create your views here.
def diary_list(request):
    grades = Grade.objects.all()
    
    return render(request, "grades/diary_list.html", {"grades": grades})


class GradeDeleteView(DeleteView):
    model = Grade
    success_url = reverse_lazy('diary/')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='moderator').exists():
            raise PermissionDenied
        
        return super().dispatch(request *args, **kwargs)


class GradeUpdateView(UpdateView):
    model = Grade
    fields = ["grade"]
    success_url = reverse_lazy("diary-list")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='moderator').exists():
            raise PermissionDenied
        
        return super().dispatch(request *args, **kwargs)
