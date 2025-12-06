from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfileModel


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматично створює профіль при створенні нового користувача"""
    if created:
        ProfileModel.objects.create(
            user=instance,
            nickname=instance.username,
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Зберігає профіль при збереженні користувача"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
