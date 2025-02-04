from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class ArtistAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Add artist-specific fields here, e.g.,
    # bio = models.TextField(blank=True)

    class Meta:
        db_table = 'artist_user'

@receiver(post_save, sender=User)
def create_or_update_artist_account(sender, instance, created, **kwargs):
    if instance.is_staff: # Check if instance is staff and ready
        if created:
            ArtistAccount.objects.create(user=instance)  # Create when User is created
        else:
            instance.artistaccount.save() #This code will work in tandem with that code.

class Album(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Music(models.Model):
    artist = models.ForeignKey(ArtistAccount, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    music_name = models.CharField(max_length=255)
    music_date = models.DateField()
    audio_file = models.FileField(upload_to='media/', validators=[])
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.music_name} - {self.artist.user.username}" # We call to the username

    class Meta:
        db_table = 'music'