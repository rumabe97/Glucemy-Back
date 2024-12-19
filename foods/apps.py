from django.apps import AppConfig
from django.core.management import call_command

class FoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foods'

    def ready(self):
        call_command('load_foods_in_chunks', 'foods.json', chunk_size=30)
        # call_command('migrate')