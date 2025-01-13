from django import forms
from .models import Song, Album

class UploadSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'album', 'genre', 'audio_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally customize widgets or labels
        self.fields['audio_file'].widget.attrs.update({'class': 'form-control-file'})