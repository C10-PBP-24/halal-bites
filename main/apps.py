from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from . import signals  # Import signals to connect post_migrate
        post_migrate.connect(signals.load_fixture_data, sender=self)