from django.db import models


# Create your models here.
class UserModel(models.Model):
    class Roles(models.TextChoices):
        USER = 'User'
        STUDENT = 'Student'
        MOD = 'Moderator'
        ADMIN = 'Admin'
        

    username = models.TextField(max_length=20)
    bio = models.TextField(max_length=5000, null=True, blank=True, default='No Description Provided')
    role = models.CharField(choices=Roles.choices, default=Roles.USER)
    profile_picture = models.ImageField()


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username