from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.generic import DeletePage, FormPage
from core.permissions import ManagerRequiredMixin

from .forms import BallotForm, VoteForm
from .models import Ballot, Vote


def vote_list(request):
    votes = Vote.objects.annotate(n_ballots=Count("ballots"))
    return render(request, "votes/vote_list.html", {"votes": votes})


def vote_detail(request, pk):
    vote = get_object_or_404(Vote, pk=pk)
    my_ballot = None
    if request.user.is_authenticated:
        my_ballot = Ballot.objects.filter(vote=vote, user=request.user).first()

    is_post = request.method == "POST"
    form = BallotForm(vote, request.POST if is_post else None,
                      initial={"option": my_ballot.option_id if my_ballot else None})
    if is_post:
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if form.is_valid():
            # переголосування замінює попередній голос
            Ballot.objects.update_or_create(vote=vote, user=request.user,
                                            defaults={"option": form.cleaned_data["option"]})
            messages.success(request, "Ваш голос враховано.")
            return redirect("vote-detail", pk=pk)

    options = list(vote.options.annotate(n=Count("ballots")))
    total = sum(o.n for o in options)
    for option in options:
        option.percent = round(option.n * 100 / total) if total else 0
    return render(request, "votes/vote_detail.html", {
        "vote": vote, "form": form, "options": options, "total": total, "my_ballot": my_ballot,
    })


class VoteCreate(ManagerRequiredMixin, FormPage, CreateView):
    model = Vote
    form_class = VoteForm
    page_title = "Нове голосування"


class VoteUpdate(ManagerRequiredMixin, FormPage, UpdateView):
    model = Vote
    form_class = VoteForm
    page_title = "Редагування голосування"
    delete_url_name = "vote-delete"


class VoteDelete(ManagerRequiredMixin, DeletePage, DeleteView):
    model = Vote
    success_url = reverse_lazy("vote-list")
