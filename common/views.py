from django.views import View
from django.http import JsonResponse
from common.models import Region, District

class RegionListView(View):
    def get(self, request, *args, **kwargs):
        regions = Region.objects
        region_list = list(regions.values('id', 'name'))
        return JsonResponse({'regions': region_list})

class DistrictListView(View):
    def get(self, request, *args, **kwargs):
        region_id = request.GET.get('region_id')
        if region_id:
            districts = District.objects.filter(region_id=region_id)
            district_list = list(districts.values('id', 'name'))
            return JsonResponse({'districts': district_list})
        else:
            return JsonResponse({'error': 'region_id not provided'}, status=400)