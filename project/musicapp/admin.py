from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Music, Album, ArtistAccount, UserAccount, Playlist
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MusicInline(admin.TabularInline): # This shows the music with Album list
    model = Music
    extra = 0  # Number of empty forms to display for adding new songs
    #You can modify and add fields over here, but it is good practice to put it at the model's forms rather than this one.

class AlbumAdmin(admin.ModelAdmin):
    inlines = [MusicInline] #This AlbumAdmin, has Music list inside of it
    list_display = ('name',) # display albums by name

    def delete_queryset(self, request, queryset):
        # Override the default delete_queryset to delete the audio file from the media directory
        for obj in queryset:
            self.delete_model(request, obj)

    def delete_model(self, request, obj):
        # First, get all music associated with the album
        tracks = Music.objects.filter(album=obj)

        # Iterate through the tracks and delete their audio files and database entries
        for track in tracks:
            if track.audio_file:
                audio_file_path = os.path.join(settings.MEDIA_ROOT, track.audio_file.name)
                if os.path.exists(audio_file_path):
                    try:
                        os.remove(audio_file_path)
                    except OSError as e:
                        logger.error(f"Error deleting audio file for track {track.music_name}: {e}")

            # Delete the track from the database
            track.delete()

        # Delete the cover image of the Album
        if obj.cover_image:
            cover_image_path = os.path.join(settings.MEDIA_ROOT, obj.cover_image.name)
            if os.path.exists(cover_image_path):
                try:
                    os.remove(cover_image_path)
                except OSError as e:
                    logger.error(f"Error deleting cover image for album {obj.name}: {e}")

        # Finally, delete the Album object itself
        super().delete_model(request, obj)


class MusicAdmin(admin.ModelAdmin):
    list_display = ('music_name', 'artist', 'album')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

    def delete_model(self, request, obj):
        if obj.audio_file:
            audio_file_path = os.path.join(settings.MEDIA_ROOT, obj.audio_file.name)
            if os.path.exists(audio_file_path):
                try:
                    os.remove(audio_file_path)
                except OSError as e:
                    logger.error(f"Error deleting audio file for track {obj.music_name}: {e}")

        super().delete_model(request, obj)


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(User) # Unregister the default UserAdmin
admin.site.register(User, CustomUserAdmin) # Register our custom UserAdmin
admin.site.register(Music, MusicAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ArtistAccount)
admin.site.register(UserAccount)
admin.site.register(Playlist)