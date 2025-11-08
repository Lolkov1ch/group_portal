from django.db import models
from django.contrib.auth.models import User

class Category(models.Model): # категорія форуму
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class ForumThread(models.Model): # тема форуму 
    category = models.ForeignKey(Category, related_name='threads', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return f'{self.title} ({self.category.name})'

class ForumPost(models.Model): # повідомлення форуму
    thread = models.ForeignKey(ForumThread, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Post by {self.author.username} in {self.thread.title}'

class Comment(models.Model): # коментар до теми
    post = models.ForeignKey(ForumPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username}'

class Tag(models.Model): # тег для теми
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ForumThreadTag(models.Model): # штукенція шоб все працювало
    thread = models.ForeignKey(ForumThread, related_name='tags', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='threads', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('thread', 'tag')

    def __str__(self):
        return f'{self.thread.title} tagged with {self.tag.name}'

class Like(models.Model): # лайки
    post = models.ForeignKey(ForumPost, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.post.thread.title}'

class Dislike(models.Model): # дизлайки 
    post = models.ForeignKey(ForumPost, related_name='dislikes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='dislikes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.username} dislikes {self.post.thread.title}'

class Attachment(models.Model): # фоточки і файлики всякі
    post = models.ForeignKey(ForumPost, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Attachment for {self.post.thread.title}'

class ForumSettings(models.Model): # налаштування форуму, потом буду доробляти
    allow_anonymous_posts = models.BooleanField(default=False)
    max_post_length = models.PositiveIntegerField(default=5000)
    enable_likes = models.BooleanField(default=True)
    enable_dislikes = models.BooleanField(default=True)
    enable_attachments = models.BooleanField(default=True)
    posts_per_page = models.PositiveIntegerField(default=20)

    def __str__(self):
        return 'Forum Settings'

    class Meta:
        verbose_name = 'Forum Setting'
        verbose_name_plural = 'Forum Settings'