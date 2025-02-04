from django import forms
from .models import Music, Album

class UploadSongForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['music_name', 'music_date', 'album', 'audio_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the album field with Album instances
        self.fields['album'].queryset = Album.objects.all()
        self.fields['album'].empty_label = "Select an album"  # Add an empty selection
        self.fields['audio_file'].widget.attrs.update({'class': 'form-control-file'})