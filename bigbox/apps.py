from django.apps import AppConfig


class BigboxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bigbox'
    def ready(self):
        import bigbox.signals