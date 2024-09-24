import json
import os
from django.urls import reverse_lazy
import pandas as pd
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import PasportForm, WaterLevelForm
from .models import *
from openpyxl import load_workbook

TEMPLATE_DIR = 'hydrogeological'
URL_NAME = 'hydrogeological'

class PasportView(LoginRequiredMixin, FormView):
    form_class = PasportForm
    template_name = os.path.join(TEMPLATE_DIR, 'pasport.html')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Muvaffaqiyatli saqlandi')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Xatolik yuz berdi')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy(f'{URL_NAME}:pasport')
    
    
class GroundWaterLevelView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'ground_water_level.html')
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data'))
        for row in data:
            form = WaterLevelForm(row)
            if form.is_valid():
                year = form.cleaned_data['year']
                well = form.cleaned_data['well']
            # Check if a record with the same year already exists
                existing_record = WaterLevel.objects.filter(year=year, well=well).first()
                if existing_record:
                    # Update existing record with the new data
                    form = WaterLevelForm(row, instance=existing_record)
                    messages.success(self.request, f'{existing_record.year} yilgi malumotlar yangilandi')
                form.save()
        messages.success(self.request, 'Muvaffaqiyatli saqlandi')
        return JsonResponse({'status': 'success'})
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[""] = ''
        return context

class GroundWaterChemicalView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'ground_water_chemical.html')

def station(request):
    stations = Station.objects.all()
    return JsonResponse({'status': 'success', 'stations':[{'id':station.id, 'name':station.name} for station in stations]})

def well(request):
    wells = Well.objects.all()
    return JsonResponse({'status': 'success', 'wells':[{'id':well.id, 'name':well.well_number} for well in wells]})

def station_well(request):
    station_id = request.GET.get('station_id')
    if station_id:
        
        try:
            station_id = int(station_id)
        except ValueError:
            return JsonResponse({'status': 'failed', 'error_message': 'Invalid station ID'})
        
        wells = Well.objects.filter(station__id=station_id)
        
        if not wells:
            return JsonResponse({'status': 'failed', 'error_message': 'No wells found for the given station'})
        
        return JsonResponse({'status': 'success', 'wells':[{'id':well.id, 'well_number':well.well_number} for well in wells]})
    
    return JsonResponse({'status': 'failed', 'error_message': 'Station ID is required'})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'home.html')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buttons'] = [
            {'text':"Kuzatuv-burg'u qudug'i pasporti",'url':f'{URL_NAME}:pasport'},
            {'text':"Yerosti suvlari sathi rejimi",'url':f'{URL_NAME}:water-level'},
            {'text':"Yerosti suvlari kimyoviy tarkibi",'url':f'{URL_NAME}:water-chemic'},
        ]
        return context



class ImportView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'import.html')
    

class LithologicView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('lithologic.html')