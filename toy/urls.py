"""
URL configuration for toy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .routers import router_urls
from user.views import HomePageView, RegisterView
from blog.views import (
    CreateArticleView,
    ListMyArticleView,
    UpdateArticleView,
    ArticleApprovalView,
    ArticleEditedView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("register", RegisterView.as_view(), name="register"),
    path("", HomePageView.as_view(), name="home"),
    path(
        "article/",
        login_required(CreateArticleView.as_view(), login_url="/login"),
        name="create-article",
    ),
    path(
        "article/my-articles",
        login_required(ListMyArticleView.as_view(), login_url="/login"),
        name="my-articles",
    ),
    path(
        "article/<pk>/edit/",
        login_required(UpdateArticleView.as_view(), login_url="/login"),
        name="update-article",
    ),
    path(
        "article-approval",
        login_required(ArticleApprovalView.as_view(), login_url="/login"),
        name="article-approval",
    ),
    path(
        "article-approval/<pk>/",
        login_required(ArticleApprovalView.as_view(), login_url="/login"),
        name="article-approval",
    ),
    path(
        "articles-edited",
        login_required(ArticleEditedView.as_view(), login_url="/login"),
        name="articles-edited",
    ),
    path("api/", include(router_urls)),
]
