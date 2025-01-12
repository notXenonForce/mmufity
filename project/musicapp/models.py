from django.db import models
from django.contrib.auth.hashers import make_password

class UserAccount(models.Model):
    id = models.BigAutoField(primary_key=True)  # Auto-incrementing ID
    username = models.CharField(max_length=150, unique=True)  # Unique username
    email = models.EmailField(unique=True)  # Unique email
    password = models.CharField(max_length=128)  # Store passwords securely in production
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.password.startswith('pbkdf2_'):  # Avoid re-hashing an already hashed password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username

    class Meta: # <--- Corrected Indentation here
        db_table = 'user_accounts'  # Links to the database table


class ArtistAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.password.startswith('pbkdf2_'):  # Avoid re-hashing an already hashed password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username

    class Meta: # <--- Corrected Indentation here
        db_table = 'artist_accounts'

class Music(models.Model):
    id = models.BigAutoField(primary_key=True)
    artist = models.ForeignKey(ArtistAccount, on_delete=models.CASCADE)
    music_name = models.CharField(max_length=255)
    music_genre = models.CharField(max_length=100)
    music_date = models.DateField()
    audio_file = models.FileField(upload_to='music/')
    upload_date = models.DateTimeField(auto_now_add=True) # Added field for when the song was uploaded

    def __str__(self):
        return f"{self.music_name} - {self.artist.username}"

    class Meta:
        db_table = 'music'