from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Forum(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='forums')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Topic(BaseModel):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

class Post(BaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.pk:
            self.is_edited = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.author.username if self.author else 'Unknown'}"
