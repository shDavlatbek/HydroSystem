from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Add data from a text file to a specified model in the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The path to the text file containing data')
        parser.add_argument('app_name', type=str, help='The name of the app the model belongs to add data to')
        parser.add_argument('model_name', type=str, help='The name of the model to add data to')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        app_name = kwargs['app_name']
        model_name = kwargs['model_name']

        try:
            # Dynamically get the model class
            ModelClass = apps.get_model(app_name, model_name)
        except LookupError:
            self.stderr.write(self.style.ERROR(f'Model "{model_name}" not found in app "{app_name}".'))
            return

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parameter_name = line.strip()
                if parameter_name:
                    ModelClass.objects.get_or_create(name=parameter_name)
                    self.stdout.write(self.style.SUCCESS(f'Successfully added "{parameter_name}" to model "{model_name}"'))