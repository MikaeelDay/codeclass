from django.conf import settings
from django.db import models


class Submission(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    title = models.CharField(max_length=150, blank=True)
    code = models.TextField()
    output = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    instructor_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title or 'بدون عنوان'} — {self.student.username}"
