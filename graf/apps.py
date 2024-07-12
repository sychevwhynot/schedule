from django.apps import AppConfig


class GrafConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graf'

    def ready(self):
        import graf.templatetags.custom_filters
