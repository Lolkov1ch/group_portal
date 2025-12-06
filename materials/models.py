from django.db import models
from django.contrib.auth.models import User

import re

class MaterialCategory(models.Model):
    title = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.title

class Material(models.Model):
    class FileTypeChoices(models.TextChoices):
        FILE = "file", "Файл"
        LINK = "link", "Посилання"
        VIDEO = "video", "Відео"

    class IsPublishedChoices(models.TextChoices):
        PUBLISHED = "published", "Опубліковано"
        NOT_PUBLISHED = "not_published", "Не опубліковано"

    class EngineChoices(models.TextChoices):
        PYGAME = "pygame", "Pygame"
        RENPY = "renpy", "Ren'Py"
        UNITY = "unity", "Unity"
        UNREAL = "unreal", "Unreal Engine"
        GODOT = "godot", "Godot"
        GAME_MAKER = "gamemaker", "GameMaker"
        CONSTRUCT = "construct", "Construct 3"
        CUSTOM = "custom", "Власний рушій / Без рушія"
        OTHER = "other", "Інше"

    title = models.CharField(max_length=128,
                             verbose_name="Заголовок"
    )

    description = models.TextField(blank=True,
                                   verbose_name="Опис")
    
    category = models.ForeignKey(MaterialCategory,
                                 on_delete=models.CASCADE,
                                 verbose_name="Категорія"
    )

    engine = models.CharField(max_length=64,
                              choices=EngineChoices.choices,
                              verbose_name="Рушій"
    )
    
    file_type = models.CharField(max_length=16,
                                 choices=FileTypeChoices.choices,
                                 verbose_name="Тип файлу"
    )

    file_link = models.URLField(blank=True,
                                null=True,
                                verbose_name="Посилання"
    )
    
    file_upload = models.FileField(upload_to="materials/",
                                   blank=True,
                                   null=True,
                                   verbose_name="Файл"
    )

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name="Автор"
    )

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Створено"
    )

    is_published = models.CharField(max_length=20,
                                    choices=IsPublishedChoices.choices,
                                    default=IsPublishedChoices.PUBLISHED,
                                    verbose_name="Статус публікації"
    )

    class Meta:
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.file_type}"
    
    @property
    def youtube_id(self):
        """Витягує ID YouTube відео з посилання"""
        if not self.file_link:
            return None
        regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(regex, self.file_link)
        return match.group(1) if match else None
    
    def get_icon(self):
        """Повертає CSS-клас іконки (Bootstrap Icons)"""
        if self.file_type == self.FileTypeChoices.VIDEO:
            return "bi bi-youtube"
        elif self.file_type == self.FileTypeChoices.FILE:
            if self.file_upload and self.file_upload.name.endswith('.zip'):
                return "bi bi-file-earmark-zip"
            return "bi bi-file-earmark-text"
        elif self.file_type == self.FileTypeChoices.LINK:
            return "bi bi-link-45deg"
        return "bi bi-question-circle"

    def get_badge_color(self):
        """Повертає Bootstrap-клас кольору для бейджа"""
        match self.engine:
            case self.EngineChoices.UNITY:
                return "bg-secondary"         # Сірий
            case self.EngineChoices.UNREAL:
                return "bg-dark"              # Чорний
            case self.EngineChoices.GODOT:
                return "bg-primary"           # Синій
            case self.EngineChoices.PYGAME:
                return "bg-warning text-dark" # Жовтий
            case _:
                return "bg-info"