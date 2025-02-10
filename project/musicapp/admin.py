from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Music, Album, ArtistAccount, UserAccount

class MusicInline(admin.TabularInline): # This shows the music with Album list
    model = Music
    extra = 0  # Number of empty forms to display for adding new songs
    #You can modify and add fields over here, but it is good practice to put it at the model's forms rather than this one.

class AlbumAdmin(admin.ModelAdmin):
    inlines = [MusicInline] #This AlbumAdmin, has Music list inside of it
    list_display = ('name',) # display albums by name

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
admin.site.register(Music)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ArtistAccount)
admin.site.register(UserAccount)