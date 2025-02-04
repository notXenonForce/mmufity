from django.core.exceptions import ValidationError

def validate_audio_file(value):  # value is the FileField
    import os
    from pathlib import Path

    ext = Path(value.name).suffix
    valid_extensions = ['.mp3', '.mp4']  # Allow both MP3 and MP4
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only MP3 and MP4 are allowed.')