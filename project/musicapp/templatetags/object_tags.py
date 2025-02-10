from django import template
from musicapp.models import Album, ArtistAccount, Music

register = template.Library()

@register.filter(name='object_type')
def object_type(value):
    if isinstance(value, Album):
        return "Album"
    elif isinstance(value, ArtistAccount):
        return "ArtistAccount"
    elif isinstance(value, Music):
        return "Music"
    else:
        return "Unknown"