from django.core.management.base import BaseCommand
from hydrogeological.models import Station  # Replace 'yourapp' with the actual name of your Django app

class Command(BaseCommand):
    help = 'Add stations from list.txt to the Station model'

    def handle(self, *args, **kwargs):
        file_path = 'list.txt'  # Path to your list.txt file
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                station_name = line.strip()
                if station_name:
                    WellType.objects.get_or_create(name=station_name)
        
        self.stdout.write(self.style.SUCCESS('Stations added successfully'))
        