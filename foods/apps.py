from django.apps import AppConfig
from django.core.management import call_command
import json
import os


class FoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foods'

    def ready(self):
        # self.load_food()
        call_command('migrate')

    def load_food(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        fixtures_path = os.path.join(base_dir, 'fixtures', 'foods.json')
        with open(fixtures_path, 'r') as file:
            data = json.load(file)

        foods = []
        from foods.models import Foods
        for item in data:
            foods.append(Foods(
                id=item['pk'],
                name=item['fields'].get('name', 'Desconocido'),
                usual_measure=item['fields'].get('usual_measure', 0.0),
                hc_rations=item['fields'].get('hc_rations', 0.0),
                glycemic_index=item['fields'].get('glycemic_index', 0),
            ))

        Foods.objects.bulk_create(foods)
