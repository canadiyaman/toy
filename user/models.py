from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

__all__ = ["Writer"]


class Writer(AbstractUser):

    REQUIRED_FIELDS = []

    is_editor = models.BooleanField()
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"
