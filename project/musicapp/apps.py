from django.apps import AppConfig

class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'musicapp'
    def ready(self):
        import musicapp.signals