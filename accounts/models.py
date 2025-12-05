from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class GenreItem(models.Model):
    genre = models.CharField(max_length=200, null=True)


class ProfileModel(models.Model):
    class Roles(models.TextChoices):
        USER = 'User'
        STUDENT = 'Student'
        MOD = 'Moderator'
        ADMIN = 'Admin'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='User'
    )

    nickname = models.TextField(max_length=20)
    about = models.TextField(max_length=5000, null=True, blank=True, default='No Description Provided')
    role = models.CharField(choices=Roles.choices, default=Roles.USER)
    favourite_genres = models.ManyToManyField(GenreItem, null=True)
    favourite_game = models.TextField(max_length=50, default='None')
    github_link = models.URLField(max_length=500, null=True)
    profile_picture = models.ImageField()


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username