import io
import json
import os
from django.urls import reverse_lazy
import pandas as pd
from django.views.generic import TemplateView, FormView, View
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse

from helper.analysis import process_request
from .forms import MeteorologyForm, HydrometriaForm
from .models import *
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import time

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
    
    def post(self, request, *args, **kwargs):
        hydropost_id = request.POST.get('hydropost_id')
        mode_id = request.POST.get('mode_id')
        
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        start_month = request.POST.get('start_month')
        end_month = request.POST.get('end_month')
        
        try: hydropost_id = int(hydropost_id)
        except: return JsonResponse({'status': 'error', 'message': 'Invalid hydropost ID'})
        
        res = process_request('hydrometeorological', "HydropostValue", start_year, end_year, start_month, end_month, hydropost=hydropost_id, mode=mode_id)
        
        return JsonResponse({
            **res
        })


class GraphOneYear(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.POST.get('data'):
            return JsonResponse({'success': 'error', 'message': 'Empty data'})
        
        df = pd.DataFrame(json.loads(request.POST.get('data')))
        year = request.POST.get('year')
        hydropost_id = request.POST.get('hydropost_id')
        mode_id = request.POST.get('mode_id')

        if year not in df['year'].values:
            return JsonResponse({'success': 'error', 'message': 'Year not found'})

        # Set the backend for matplotlib
        plt.switch_backend('agg')

        # Filter data for the selected year and prepare it for plotting
        year_to_plot = year
        df_year = df[df['year'] == year_to_plot].drop(columns='year').T  # Drop the 'year' column and transpose
        df_year.columns = [year_to_plot]  # Rename the column to the year

        # Extract x and y values for plotting
        x = np.arange(len(df_year))
        y = df_year[year_to_plot].values

        # Function to plot segments
        def plot_segments(x, y, color, label):
            # Identify segments based on NaN values
            mask = ~np.isnan(y)  # Create a mask of valid (non-NaN) values
            segments = np.split(y[mask], np.where(np.diff(mask) == -1)[0] + 1)
            x_segments = np.split(x[mask], np.where(np.diff(mask) == -1)[0] + 1)

            # Plot each segment
            for x_seg, y_seg in zip(x_segments, segments):
                if len(x_seg) > 1:  # Ensure there's more than one point to plot
                    plt.plot(x_seg, y_seg, linestyle='solid', color=color, label=label)

        # Plot the segments for the year
        plt.figure(figsize=(12, 6))
        plot_segments(x, y, color='b', label=year_to_plot)

        # Set the title and labels
        title = f'{Mode.objects.filter(id=mode_id).first().name} {str(Hydropost.objects.filter(id=hydropost_id).first().name) + " - " if hydropost_id else ""}{year_to_plot} yil'
        plt.title(label=title, y=1.05)
        plt.grid()
        plt.xlabel('Oylar')
        plt.ylabel('Sathi')

        # Save the plot to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=480)
        plt.close()

        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{title}.png"'
        return response

class GraphCompareTwoYears(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.POST.get('data'): 
            return JsonResponse({'success': 'error', 'message': 'Empty data'})
        
        df = pd.DataFrame(json.loads(request.POST.get('data')))
        year1 = request.POST.get('year')
        year2 = request.POST.get('compare_year')
        hydropost_id = request.POST.get('hydropost_id')
        mode_id = request.POST.get('mode_id')
        
        if year1 not in df['year'].values or year2 not in df['year'].values:
            return JsonResponse({'success': 'error', 'message': 'One or both years not found'})
        
        matplotlib.use('agg')

        # Prepare data for the first year
        df_year1 = df[df['year'] == year1].drop(columns='year').T
        df_year1.columns = [year1]
        
        # Prepare data for the second year
        df_year2 = df[df['year'] == year2].drop(columns='year').T
        df_year2.columns = [year2]

        # Function to plot segments
        def plot_segments(x, y, color, label):
            # Identify segments based on NaN values
            mask = ~np.isnan(y)  # Create a mask of valid (non-NaN) values
            segments = np.split(y[mask], np.where(np.diff(mask) == -1)[0] + 1)
            x_segments = np.split(x[mask], np.where(np.diff(mask) == -1)[0] + 1)

            # Plot each segment
            for x_seg, y_seg in zip(x_segments, segments):
                if len(x_seg) > 1:  # Ensure there's more than one point to plot
                    plt.plot(x_seg, y_seg, linestyle='solid', color=color, label=label)

        # Extract x values
        x = np.arange(len(df_year1))

        # Plot the segments for both years
        plt.figure(figsize=(12, 6))  # Set the figure size
        plot_segments(x, df_year1[year1].values, color='b', label=year1)
        plot_segments(x, df_year2[year2].values, color='r', label=year2)

        # Set the title and labels
        title = f'{Mode.objects.filter(id=mode_id).first().name} {str(Hydropost.objects.filter(id=hydropost_id).first().name) + " - " if hydropost_id else ""}{year1} yil va {year2} yil'
        plt.title(label=title, y=1.05)
        plt.grid()
        plt.xlabel('Oylar')
        plt.ylabel('Sathi')
        plt.legend()  # Add a legend to differentiate between the years
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=480)
        plt.close()

        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{title}.png"'
        return response