from django.db import models

from user.models import Writer

__all__ = ["Article"]


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    written_by = models.ForeignKey(
        Writer, on_delete=models.CASCADE, related_name="writer_articles"
    )
    edited_by = models.ForeignKey(
        Writer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="editor_articles",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    APPROVED = "approved"
    REJECTED = "rejected"
    DRAFT = "draft"

    STATUSES = ((APPROVED, "Approved"), (REJECTED, "Rejected"), (DRAFT, "Draft"))

    status = models.CharField(max_length=8, choices=STATUSES, default=DRAFT)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
