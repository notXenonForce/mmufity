from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
import os
from django.core.files.storage import default_storage

class ArtistAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=150, blank=True, null=True)  # Add username field
    email = models.EmailField(blank=True, null=True)  # Add email field
    banner_image = models.ImageField(upload_to='banners/', blank=True, null=True) #added upload_to

    class Meta:
        db_table = 'artist_user'

    def __str__(self):
        return self.user.username

@receiver(pre_save, sender=ArtistAccount)
def delete_old_banner(sender, instance, **kwargs):
    """Deletes the old banner image when a new banner is uploaded."""
    if instance.pk:
        try:
            old_instance = ArtistAccount.objects.get(pk=instance.pk)
            if old_instance.banner_image and instance.banner_image != old_instance.banner_image:
                # Delete the old image
                if default_storage.exists(old_instance.banner_image.name):
                    default_storage.delete(old_instance.banner_image.name)
        except ArtistAccount.DoesNotExist:
            pass  # Handle the case where the old instance does not exist


class Album(models.Model):
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='album_covers/', null=True, blank=True)  # Add album cover image

    def __str__(self):
        return self.name

class Music(models.Model):
    artist = models.ForeignKey(ArtistAccount, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    music_name = models.CharField(max_length=255)
    music_date = models.DateField()
    audio_file = models.FileField(upload_to='songs/', validators=[])
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.music_name} - {self.artist.user.username}" # We call to the username

    class Meta:
        db_table = 'music'

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='album_covers/', null=True, blank=True)  # Add album cover image

    def __str__(self):
        return self.name