from django.core.management.base import BaseCommand
from django.core.management import call_command
import json
from myapp.models import Food


class Command(BaseCommand):
    help = 'Carga los registros de foods.json en bloques (chunks) para mejorar la eficiencia'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo de fixtures JSON')
        parser.add_argument('--chunk_size', type=int, default=20, help='Tamaño del bloque de registros a insertar')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        chunk_size = kwargs['chunk_size']

        with open(json_file, 'r') as f:
            data = json.load(f)

        foods = []
        for item in data:
            foods.append(Food(
                id=item['pk'],
                name=item['fields']['name'],
                usual_measure=item['fields']['usual_measure'],
                hc_rations=item['fields']['hc_rations'],
                glycemic_index=item['fields']['glycemic_index'],
            ))

            if len(foods) >= chunk_size:
                Food.objects.bulk_create(foods)
                foods = []

        if foods:
            Food.objects.bulk_create(foods)

        self.stdout.write(self.style.SUCCESS(f'Carga completa de {len(data)} registros en bloques de {chunk_size}.'))
