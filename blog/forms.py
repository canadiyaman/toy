from django.forms import ModelForm

from .models import Article


class CustomCreateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.written_by = self.user
        if commit:
            user.save()
        return user


class CustomUpdateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        article = super().save(commit=False)
        article.edited_by = self.user
        if commit:
            article.save()
        return article
