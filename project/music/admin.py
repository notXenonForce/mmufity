from django.contrib import admin
from .models import UserAccount, ArtistAccount

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')  # Display these columns in the admin list view
    search_fields = ('username', 'email')  # Add a search bar for username and email
    exclude = ('password',)

@admin.register(ArtistAccount)
class ArtistAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')
    exclude = ('password',)