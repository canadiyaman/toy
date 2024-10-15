from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Article
from .forms import CustomCreateArticleForm, CustomUpdateArticleForm
from .serializers import ArticleSerializer


class ArticleViewset(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]


class CreateArticleView(CreateView):
    queryset = Article.objects.all()
    template_name = "article/create.html"
    form_class = CustomCreateArticleForm
    success_url = "/"

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "user": self.request.user,
                }
            )
        return kwargs


class ListMyArticleView(ListView):
    queryset = Article.objects.all()
    template_name = "article/list.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(written_by=self.request.user)
        return queryset


class UpdateArticleView(UpdateView):
    queryset = Article.objects.all()
    template_name = "article/update.html"
    form_class = CustomUpdateArticleForm
    success_url = "/article/my-articles"

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "user": self.request.user,
                }
            )
        return kwargs


class ArticleApprovalView(View):

    def get(self, request):
        if not request.user.is_editor:
            messages.error(request, "You don't have permission to see this page")
            return HttpResponseRedirect(reverse("home"))

        articles = Article.objects.filter(status=Article.DRAFT)
        context = {"articles": articles}
        return render(request, "article/approval.html", context)

    def post(self, request, pk):
        if not request.user.is_editor:
            messages.error(request, "You don't have permission to see this page")
            return HttpResponseRedirect(reverse("home"))

        article = Article.objects.get(id=pk)
        if "reject" in request.POST:
            article.status = Article.REJECTED
        elif "approve" in request.POST:
            article.status = Article.APPROVED
        else:
            messages.error(request, "Bad Request")
            return HttpResponseRedirect(reverse("article-approval"))

        article.edited_by = request.user
        article.save(update_fields=["status", "edited_by"])
        messages.success(request, f"{article.title} updated successfully")
        return HttpResponseRedirect(reverse("article-approval"))


class ArticleEditedView(View):

    def get(self, request):
        if not request.user.is_editor:
            messages.error(request, "You don't have permission to see this page")
            return HttpResponseRedirect(reverse("home"))

        articles = Article.objects.filter(edited_by__is_editor=True)
        context = {"articles": articles}
        return render(request, "article/edited.html", context)
