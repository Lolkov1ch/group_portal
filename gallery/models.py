from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from gallery.utils import gallery_image_path


class MediaItem(models.Model):

    MEDIA_TYPES = [
        ("photo", "Фото"),
        ("screenshot", "Скріншот"),
        ("video", "Відео"),
        ("other", "Інше"),
        ("unknown", "Не вказано"),
    ]

    ALLOWED_EXTENSIONS = [
        "png", "jpg", "jpeg", "gif",
        "mp4", "mov", "avi", "mkv",
        "webm"
    ]

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    file = models.FileField(upload_to=gallery_image_path)

    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default="unknown")
    game_name = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_approved = models.BooleanField(default=False)

    def clean(self):
        if not self.file:
            return

        filename = self.file.name
        ext = filename.split(".")[-1].lower()

        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValidationError(
                f"Розширення '{ext}' не дозволене. "
                f"Дозволені: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )

        if self.file.size > 20 * 1024 * 1024:
            raise ValidationError("Розмір файлу не може перевищувати 20 МБ.")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def is_image(self):
        if not self.file:
            return False
        ext = self.file.name.split(".")[-1].lower()
        return ext in ["png", "jpg", "jpeg", "gif"]

    def delete(self, *args, **kwargs):
        if self.file:
            try:
                if os.path.isfile(self.file.path):
                    os.remove(self.file.path)
            except Exception as e:
                print(f"Помилка при видаленні файлу: {e}")

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Медіафайл"
        verbose_name_plural = "Медіафайли"

    def __str__(self):
        return self.title
