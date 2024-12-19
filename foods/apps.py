from django.apps import AppConfig
from django.core.management import call_command

class FoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foods'

    # def ready(self):
        # call_command('loaddata', 'foods.json', verbosity=0)
        # call_command('migrate')