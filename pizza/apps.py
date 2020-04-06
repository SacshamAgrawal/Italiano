from django.apps import AppConfig

class PizzaConfig(AppConfig):
    name = 'pizza'
    def ready(self):
        from . import signals
