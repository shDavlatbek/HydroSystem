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

TEMPLATE_DIR = 'hydromelioratical'
URL_NAME = 'hydromelioratical'

class PasportView(LoginRequiredMixin, FormView):
    form_class = PasportForm
    template_name = os.path.join(TEMPLATE_DIR, 'pasport.html')
    success_url = reverse_lazy(f'{URL_NAME}:pasport')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Muvaffaqiyatli saqlandi')
        return super().form_valid(form)

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
        return True
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[""] = ''
        return context

class GroundWaterChemicalView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'ground_water_chemical.html')

def expedicion(request):
    expedicions = Expedicion.objects.all()
    return JsonResponse({'status': 'success', 'expedicions':[{'id':expedicion.id, 'name':expedicion.name} for expedicion in expedicions]})

def well(request):
    wells = Well.objects.all()
    return JsonResponse({'status': 'success', 'wells':[{'id':well.id, 'name':well.well_number} for well in wells]})

def region_expedicion(request):
    region_id = request.GET.get('region_id')
    if region_id:
        try:
            region_id = int(region_id)
        except ValueError:
            return JsonResponse({'status': 'failed', 'error_message': 'Invalid region ID'})

        expedicions = Expedicion.objects.filter(region__id=region_id)

        if not expedicions:
            return JsonResponse({'status': 'failed', 'error_message': 'No expedicions found for the given region'})

        return JsonResponse({'status': 'success', 'expedicions':[{'id':expedicion.id, 'name':expedicion.name} for expedicion in expedicions]})

    return JsonResponse({'status': 'failed', 'error_message': 'Region ID is required'})

def expedicion_well(request):
    expedicion_id = request.GET.get('expedicion_id')
    if expedicion_id:
        
        try:
            expedicion_id = int(expedicion_id)
        except ValueError:
            return JsonResponse({'status': 'failed', 'error_message': 'Invalid expedicion ID'})
        
        wells = Well.objects.filter(expedicion__id=expedicion_id)
        
        if not wells:
            return JsonResponse({'status': 'failed', 'error_message': 'No wells found for the given expedicion'})
        
        return JsonResponse({'status': 'success', 'wells':[{'id':well.id, 'well_number':well.well_number} for well in wells]})
    
    return JsonResponse({'status': 'failed', 'error_message': 'Station ID is required'})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'home.html')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buttons'] = [
            {'text':"Gidromeliorativ ob'ekt pasporti",'url':f'{URL_NAME}:pasport'},
            {'text':"Yerosti suvlari sathi rejimi",'url':f'{URL_NAME}:water-level'},
            {'text':"Yerosti suvlari kimyoviy tarkibi",'url':f'{URL_NAME}:water-chemic'},
            {'text':"Tuproq sho'rlanish kuzatuv nuqtalari",'url':f'{URL_NAME}:water-chemic'},
        ]
        return context
    
class ImportView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'import.html')
    def post(self, request):
        try:
            file_obj = request.FILES['files']
            df = pd.read_excel(file_obj, engine='openpyxl', header=None, index_col=None)

            df = df.fillna('') 
            # df = df.iloc[1:] 

            # Convert DataFrame to HTML
            data_to_display = df.to_json(orient='records')
            # data_to_display = df.to_
            return JsonResponse({'status': 'success', 'data': data_to_display})
        
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error_message': str(e)})
