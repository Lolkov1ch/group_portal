from django.db import models
from django.contrib.auth.models import User
class BaseModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class Category(models.Model):
    name = models.CharField("Назва категорії", max_length=255, unique=True)
    description = models.TextField("Опис категорії", blank=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def __str__(self):
        return self.name

    def topics_count(self):
        from .models import Topic
        return Topic.objects.filter(forum__category=self).count()
class Forum(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='forums')
    name = models.CharField("Назва форуму", max_length=255)
    description = models.TextField("Опис форуму", blank=True)

    class Meta:
        verbose_name = "Форум"
        verbose_name_plural = "Форуми"
        ordering = ['name']

    def __str__(self):
        return self.name

class Topic(BaseModel):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField("Назва теми", max_length=255)
    views = models.PositiveIntegerField("Перегляди", default=0)

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Теми"
        ordering = ['-updated_at']

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
            self.is_edited = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.author.username if self.author else 'Unknown'}"
