import json
import os
from django.urls import reverse_lazy
import pandas as pd
from django.views.generic import TemplateView, FormView, View
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import MeteorologyForm, HydrometriaForm
from .models import *
from openpyxl import load_workbook

TEMPLATE_DIR = 'hydrometeorological'
URL_NAME = 'hydrometeorological'

# class GroundWaterLevelView(LoginRequiredMixin, TemplateView):
#     template_name = os.path.join(TEMPLATE_DIR, 'ground_water_level.html')
    
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.POST.get('data'))
#         for row in data:
#             form = WaterLevelForm(row)
#             if form.is_valid():
#                 year = form.cleaned_data['year']
#                 well = form.cleaned_data['well']
#             # Check if a record with the same year already exists
#                 existing_record = WaterLevel.objects.filter(year=year, well=well).first()
#                 if existing_record:
#                     # Update existing record with the new data
#                     form = WaterLevelForm(row, instance=existing_record)
#                     messages.success(self.request, f'{existing_record.year} yilgi malumotlar yangilandi')
#                 form.save()
#         messages.success(self.request, 'Muvaffaqiyatli saqlandi')
#         return JsonResponse({'status': 'success'})
        
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context[""] = ''
#         return context

# class GroundWaterChemicalView(LoginRequiredMixin, TemplateView):
#     template_name = os.path.join(TEMPLATE_DIR, 'ground_water_chemical.html')

# def expedicion(request):
#     expedicions = Expedicion.objects.all()
#     return JsonResponse({'status': 'success', 'expedicions':[{'id':expedicion.id, 'name':expedicion.name} for expedicion in expedicions]})

# def well(request):
#     wells = Well.objects.all()
#     return JsonResponse({'status': 'success', 'wells':[{'id':well.id, 'name':well.well_number} for well in wells]})

# def region_expedicion(request):
#     region_id = request.GET.get('region_id')
#     if region_id:
#         try:
#             region_id = int(region_id)
#         except ValueError:
#             return JsonResponse({'status': 'failed', 'error_message': 'Invalid region ID'})

#         expedicions = Expedicion.objects.filter(region__id=region_id)

#         if not expedicions:
#             return JsonResponse({'status': 'failed', 'error_message': 'No expedicions found for the given region'})

#         return JsonResponse({'status': 'success', 'expedicions':[{'id':expedicion.id, 'name':expedicion.name} for expedicion in expedicions]})

#     return JsonResponse({'status': 'failed', 'error_message': 'Region ID is required'})

# def expedicion_well(request):
#     expedicion_id = request.GET.get('expedicion_id')
#     if expedicion_id:
        
#         try:
#             expedicion_id = int(expedicion_id)
#         except ValueError:
#             return JsonResponse({'status': 'failed', 'error_message': 'Invalid expedicion ID'})
        
#         wells = Well.objects.filter(expedicion__id=expedicion_id)
        
#         if not wells:
#             return JsonResponse({'status': 'failed', 'error_message': 'No wells found for the given expedicion'})
        
#         return JsonResponse({'status': 'success', 'wells':[{'id':well.id, 'well_number':well.well_number} for well in wells]})
    
#     return JsonResponse({'status': 'failed', 'error_message': 'Station ID is required'})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'home.html')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buttons'] = [
            {'text':"Gidrometriya",'url':f'{URL_NAME}:hydrometria'},
            {'text':"Meteorologiya",'url':f'{URL_NAME}:meteorology'}
        ]
        return context

class MeteorologyView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'meteorology.html')
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data'))
        for row in data:
            form = MeteorologyForm(row)
            if form.is_valid():
                year = form.cleaned_data['year']
                parameter = form.cleaned_data['parameter']
                meteostation = form.cleaned_data['meteostation']
            # Check if a record with the same year already exists
                existing_record = MeteostationValue.objects.filter(year=year, meteostation=meteostation, parameter=parameter).first()
                if existing_record:
                    # Update existing record with the new data
                    form = HydrometriaForm(row, instance=existing_record)
                    messages.success(self.request, f'{existing_record.year} yilgi malumotlar yangilandi')
                form.save()
        messages.success(self.request, 'Muvaffaqiyatli saqlandi')
        return JsonResponse({'status': 'success'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MeteorologyForm()
        return context

class HydrometriaView(LoginRequiredMixin, TemplateView):
    
    template_name = os.path.join(TEMPLATE_DIR, 'hydrometria.html')
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data'))
        for row in data:
            form = HydrometriaForm(row)
            if form.is_valid():
                year = form.cleaned_data['year']
                mode = form.cleaned_data['mode']
                hydropost = form.cleaned_data['hydropost']
                object_type = form.cleaned_data['object_type']
            # Check if a record with the same year already exists
                existing_record = HydropostValue.objects.filter(year=year, hydropost=hydropost, mode=mode).first()
                if existing_record:
                    # Update existing record with the new data
                    form = HydrometriaForm(row, instance=existing_record)
                    messages.success(self.request, f'{existing_record.year} yilgi malumotlar yangilandi')
                form.save()
        messages.success(self.request, 'Muvaffaqiyatli saqlandi')
        return JsonResponse({'status': 'success'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = HydrometriaForm()
        return context
    
    
class HydrometriaShowView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'show/ground_water_level.html')