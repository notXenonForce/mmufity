from django import forms
from .models import Music, Album  # Import your Music and Album models

class UploadSongForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['music_name', 'music_date', 'album', 'audio_file']
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

class BannerUploadForm(forms.Form):
    banner_image = forms.ImageField(required=True)