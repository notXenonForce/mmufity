from .models import User, ArtistAccount
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

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

@receiver(post_save, sender=User)
def create_artist_account(sender, instance, created, **kwargs):
    print(f"I came here before for {instance.username}")  # Fix string formatting

    if created:
        print(f"Checking if {instance.username} is staff: {instance.is_staff}")  # Debugging staff status

        if instance.is_staff and not hasattr(instance, 'artistaccount'):
            ArtistAccount.objects.create(user=instance, username=instance.username, email=instance.email)
            print(f"Created ArtistAccount for {instance.username}")
