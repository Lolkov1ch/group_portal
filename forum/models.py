from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from .utils import image_path


class BaseModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField("Назва категорії", max_length=255, unique=True)
    description = models.TextField("Опис категорії", blank=True)
    is_open = models.BooleanField("Відкрита для створення тем", default=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def __str__(self):
        return self.name

    def topics_count(self):
        if not hasattr(self, '_topics_count'):
            self._topics_count = Topic.objects.filter(forum__category=self).count()
        return self._topics_count


class Forum(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='forums', null=True, blank=True)
    name = models.CharField("Назва форуму", max_length=255)
    description = models.TextField("Опис форуму", blank=True)

    class Meta:
        verbose_name = "Форум"
        verbose_name_plural = "Форуми"
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField("Назва тегу", max_length=50, unique=True)
    slug = models.SlugField("Slug", max_length=50, unique=True)
    color = models.CharField("Колір", max_length=7, default="#007bff", help_text="Hex-колір, наприклад #FF5733")
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            from unidecode import unidecode
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)


class Topic(BaseModel):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField("Назва теми", max_length=255)
    views = models.PositiveIntegerField("Перегляди", default=0)
    is_pinned = models.BooleanField("Закріплено", default=False)
    is_locked = models.BooleanField("Закрито", default=False)
    tags = models.ManyToManyField(Tag, related_name='topics', blank=True, verbose_name="Теги")
    
    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Теми"
        ordering = ['is_locked', '-is_pinned', '-updated_at']
    
    def __str__(self):
        return self.title


class Post(BaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField("Контент")
    is_edited = models.BooleanField("Редаговано", default=False)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                orig = Post.objects.get(pk=self.pk)
                if orig.content != self.content:
                    self.is_edited = True
            except Post.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.author.username if self.author else 'Unknown'}"


class ForumSettings(models.Model):
    enable_likes = models.BooleanField(default=True)
    enable_dislikes = models.BooleanField(default=True)
    enable_attachments = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Налаштування форуму"
        verbose_name_plural = "Налаштування форуму"

    def __str__(self):
        return "Forum Settings"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "post")
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="dislikes")

    class Meta:
        unique_together = ("user", "post")
        verbose_name = "Дизлайк"
        verbose_name_plural = "Дизлайки"


class Attachment(models.Model):
    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "pdf", "zip", "rar", "7z", "txt", "mp4"]
    
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to=image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.file:
            filename = self.file.name
            parts = filename.split(".")
            
            if len(parts) < 2:
                raise ValidationError("Файл повинен мати розширення.")
            
            ext = parts[-1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                raise ValidationError(
                    f"Розширення '{ext}' не дозволено. Дозволені: {', '.join(self.ALLOWED_EXTENSIONS)}"
                )
            
            if self.file.size > 20 * 1024 * 1024:
                raise ValidationError("Розмір файлу не може перевищувати 20 МБ.")

    def is_image(self):
        if not self.file:
            return False
        parts = self.file.name.split(".")
        if len(parts) < 2:
            return False
        return parts[-1].lower() in ["png", "jpg", "jpeg", "gif"]
    
    def delete(self, *args, **kwargs):
        if self.file:
            try:
                if os.path.isfile(self.file.path):
                    os.remove(self.file.path)
            except Exception as e:
                print(f"Помилка при видаленні файлу: {e}")
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Вкладення"
        verbose_name_plural = "Вкладення"

    def __str__(self):
        return self.file.name if self.file else "No file"



@receiver(post_delete, sender=Attachment)
def delete_attachment_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        try:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
        except Exception as e:
            print(f"Помилка при видаленні файлу через сигнал: {e}")


@receiver(pre_save, sender=Attachment)
def delete_old_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Attachment.objects.get(pk=instance.pk)
        if old_instance.file and old_instance.file != instance.file:
            if os.path.isfile(old_instance.file.path):
                os.remove(old_instance.file.path)
    except Attachment.DoesNotExist:
        pass
    except Exception as e:
        print(f"Помилка при видаленні старого файлу: {e}")


