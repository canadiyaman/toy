from django import forms
from .models import Writer


__all__ = ["RegisterForm"]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def clean_password(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.clean_password())
        if commit:
            user.save()
        return user

    class Meta:
        model = Writer
        fields = ["username", "password", "is_editor"]
