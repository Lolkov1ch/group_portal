from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    class FileTypeChoices(models.TextChoices):
        FILE = "file", "File"
        LINK = "link", "Link"
        VIDEO = "video", "Video"

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, blank=True)
    file_type = models.CharField(
        max_length=16,
        choices=FileTypeChoices.choices
    )
    file_link = models.CharField(max_length=512)
    subject = models.CharField(max_length=128)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)