import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from foodgram import settings
from recipes.models import Ingredient

DATA_DIR = Path(settings.DATA_DIR)


class Command(BaseCommand):
    def handle(self, *args, **options):
        def csv_to_model(csv_file, model):
            '''Читайет файлы CSV и добавляет данные в модель'''

            csv_file_path = DATA_DIR / csv_file
            with open(csv_file_path, 'r', encoding='utf-8') as data_csv_file:
                reader = csv.DictReader(data_csv_file)
                model.objects.bulk_create(model(**row) for row in reader)
                self.stdout.write(
                    self.style.SUCCESS(
                        'Данные успешно загружены из файла '
                        f'{csv_file} в модель {model.__name__}'
                    )
                )
        csv_to_model('ingredients.csv', Ingredient)
