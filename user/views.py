from datetime import datetime, timedelta

from django.contrib import messages
from django.db.models import Count, F, Case, When, IntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from blog.models import Article
from .forms import RegisterForm

__all__ = ["HomePageView", "RegisterView"]


class HomePageView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        treshold = datetime.now() - timedelta(hours=30)
        articles = (
            Article.objects.select_related("written_by")
            .values(user=F("written_by__username"))
            .annotate(
                total_article_count=Count("written_by"),
                witten_articles_last_30=Count(
                    Case(
                        When(created_at__gte=treshold, then=1),
                        output_field=IntegerField(),
                    )
                ),
            )
        )
        context = {"articles": articles}
        return render(request, "home.html", context)


class RegisterView(View):
    def get(self, request):
        context = {"form": RegisterForm()}
        return render(request, "registration/register.html", context=context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"Successfully created a new user with name {user.username}"
            )
            return HttpResponseRedirect(reverse("login"))
        context = {"form": form}
        return render(request, "registration/register.html", context)
