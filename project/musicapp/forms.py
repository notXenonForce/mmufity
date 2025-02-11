from django import forms
from .models import Music, Album, ArtistAccount, Playlist, UserAccount  # Import your Music and Album models

class UploadSongForm(forms.ModelForm):
    music_link = forms.URLField(
        label="Music Link",
        required=True,  # Make it optional if you want
        widget=forms.TextInput(attrs={'placeholder': 'Enter music link'})  # Optional: add a placeholder
    )
    class Meta:
        model = Music
        fields = ['music_name', 'music_date', 'album', 'audio_file', 'music_link']
        widgets = {
            'music_date': forms.DateInput(attrs={'type': 'date'}),  # Use a date picker
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].widget.attrs.update({'class': 'form-control-file'})


class AlbumForm(forms.ModelForm):  # Inherit from forms.ModelForm
    class Meta:
        model = Album  # Specify the associated model
        fields = ['name', 'cover_image']  # List the fields from the model to include in the form

class BannerUploadForm(forms.ModelForm):  # Now a ModelForm!
    class Meta:
        model = ArtistAccount  # Use ArtistAccount
        fields = ['banner_image']  # Only include the banner_image

class UserBannerUploadForm(forms.ModelForm):  # Create a separate form for UserAccount
    class Meta:
        model = UserAccount  # Use UserAccount
        fields = ['banner_image']  # Only include the banner_image

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'cover_image']

class EditSongForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['music_name']
        widgets = {
            'music_name': forms.TextInput(attrs={'class': 'form-control'}),
        }