import json
from django.core.management.base import BaseCommand
from common.models import Region, District

class Command(BaseCommand):
    help = 'Load regions and districts from a JSON file'

    def handle(self, *args, **kwargs):
        with open('static/js/regions.json', 'r', encoding='cp1252') as file:
            regions = json.load(file)
        
        with open('static/js/districts.json', 'r', encoding='cp1252') as file:
            districts = json.load(file)

        for region_data in regions:
            region, created = Region.objects.get_or_create(
                id=region_data['id'],
                defaults={
                    'name': region_data['name_uz']
                }
            )

        for district_data in districts:
            region = Region.objects.get(id=district_data['region_id'])
            district, created = District.objects.get_or_create(
                id=district_data['id'],
                defaults={
                    'name': district_data['name_uz'],
                    'region': region
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded regions and districts'))
