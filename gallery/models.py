from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
import logging
from gallery.utils import gallery_image_path

logger = logging.getLogger(__name__)


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

    IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

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

        if hasattr(self.file, 'size') and self.file.size > 20 * 1024 * 1024:
            raise ValidationError(
                "Файл занадто великий. Максимальний розмір: 20 МБ"
            )

    def is_image(self):
        if not self.file:
            return False
        ext = self.file.name.split(".")[-1].lower()
        return ext in self.IMAGE_EXTENSIONS

    def delete(self, *args, **kwargs):
        if self.file:
            try:
                file_path = self.file.path
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f"Файл видалено: {file_path}")
                    
                    folder_path = os.path.dirname(file_path)
                    if os.path.exists(folder_path) and not os.listdir(folder_path):
                        os.rmdir(folder_path)
                        logger.info(f"Папка видалена: {folder_path}")
                        
            except Exception as e:
                logger.error(f"Помилка при видаленні файлу: {e}")

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Медіафайл"
        verbose_name_plural = "Медіафайли"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_approved', '-created_at']),
        ]

    def __str__(self):
        return self.title