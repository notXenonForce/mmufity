from .models import User, ArtistAccount, UserAccount
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

# Signal to create ArtistAccount when a staff user is created
@receiver(post_save, sender=User)
def create_artist_account(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        if not hasattr(instance, 'artistaccount'):
            logger.info(f"Creating ArtistAccount for {instance.username}")
            ArtistAccount.objects.create(user=instance, username=instance.username, email=instance.email)
        else:
            logger.info(f"ArtistAccount already exists for {instance.username}")
    else:
        logger.info(f"User {instance.username} is not staff or not newly created")

# Signal to create NormalUserAccount when a non-staff user is created
@receiver(post_save, sender=User)
def create_normal_user_account(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        if not hasattr(instance, 'normaluseraccount'):
            logger.info(f"Creating NormalUserAccount for {instance.username}")
            UserAccount.objects.create(user=instance, username=instance.username, email=instance.email)
        else:
            logger.info(f"NormalUserAccount already exists for {instance.username}")
    else:
        logger.info(f"User {instance.username} is staff or not newly created")