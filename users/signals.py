from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Profile, User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля и генерация slug при создании пользователя"""
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(
            user=instance, 
            slug=slugify(instance.username)  
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранение профиля при обновлении данных пользователя"""
    instance.profile.save()
