from django.shortcuts import render
from .models import Post, Topic, Category
# Create your views here.

def topic_list(request):
    category = Category.objects.all()
    topics = Topic.objects.all()
    context = {
        "category": category,
        "topics": topics,
    }
    return render(request, "forum/topic_list.html", context)

