from django.contrib.auth.views import redirect_to_login
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from core.generic import DeletePage, FormPage
from core.permissions import ManagerRequiredMixin, can_manage

from .forms import CategoryForm, PostForm, TopicForm
from .models import Category, Post, Topic


def topic_list(request):
    topics = Topic.objects.select_related("author").annotate(n_posts=Count("posts")).order_by("-created_at")
    categories = Category.objects.prefetch_related(Prefetch("topics", queryset=topics))
    return render(request, "forum/topic_list.html", {"categories": categories})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic.objects.select_related("category", "author"), pk=pk)
    form = PostForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect("topic-detail", pk=pk)
    posts = topic.posts.select_related("author").order_by("created_at")
    return render(request, "forum/topic_detail.html", {"topic": topic, "posts": posts, "form": form})


# --- гілки (адміністратори та модератори) ---

class TopicCreate(ManagerRequiredMixin, FormPage, CreateView):
    model = Topic
    form_class = TopicForm
    page_title = "Нова гілка"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TopicUpdate(ManagerRequiredMixin, FormPage, UpdateView):
    model = Topic
    form_class = TopicForm
    page_title = "Редагування гілки"
    delete_url_name = "topic-delete"


class TopicDelete(ManagerRequiredMixin, DeletePage, DeleteView):
    model = Topic
    success_url = reverse_lazy("topic-list")


class CategoryCreate(ManagerRequiredMixin, FormPage, CreateView):
    model = Category
    form_class = CategoryForm
    page_title = "Новий розділ форуму"
    success_url = reverse_lazy("topic-list")


class CategoryDelete(ManagerRequiredMixin, DeletePage, DeleteView):
    model = Category
    success_url = reverse_lazy("topic-list")


# --- повідомлення: видаляє автор або модератор ---

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeletePage, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        return post.author_id == self.request.user.pk or can_manage(self.request.user)

    def get_success_url(self):
        return reverse("topic-detail", args=[self.object.topic_id])
