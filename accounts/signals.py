from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import *

gotten_user = get_user_model()


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


@receiver(post_save, sender=gotten_user)
def set_admin(sender, instance, created, **kwargs):
    admin_role = ProfileModel.Roles.ADMIN
    if created and instance.is_superuser:
        instance.role = admin_role
        instance.save()