from django.apps import AppConfig


class BackendapiAutoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backendAPI_auto'

    def ready(self):
        import backendAPI_auto.signals
