import copy
import datetime
import io
import json
import os
from django.urls import reverse_lazy
from django.views import View
import pandas as pd
import pymannkendall as mk
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse

from helper.analysis import process_request
from .forms import PasportForm, WaterLevelForm
from .models import *
import tempfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import time

TEMPLATE_DIR = str(os.path.join('hydromelioratical', 'show'))
URL_NAME = 'hydromelioratical'

class GroundWaterLevelView(TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'ground_water_level.html')
    
    def post(self, request, *args, **kwargs):
        well_id = request.POST.get('well_id')
        
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        start_month = request.POST.get('start_month')
        end_month = request.POST.get('end_month')
        
        try: well_id = int(well_id)
        except: return JsonResponse({'status': 'error', 'message': 'Invalid well ID'})
        
        res = process_request('hydromelioratical', "WaterLevel", 'well__id', well_id, start_year, end_year, start_month, end_month)
        
        return JsonResponse({
            **res
        })
        
class HeatMap(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.POST.get('data'): return JsonResponse({'success': False, 'message':'Empty data'})
        df = pd.DataFrame(json.loads(request.POST.get('data')))
        
        matplotlib.use('agg')
        plt.figure(figsize=(len(df), 8), dpi=480)
        
        try:
            sns.heatmap(df.set_index('year').T, annot=True, fmt=".1f", cmap="Blues", cbar=True,) # xticklabels=True, yticklabels=True  
        except Exception as e:
            return JsonResponse({'success': False, 'message':e})
        # title and labels
        # plt.title('Heatmap')
        plt.xlabel('')
        # plt.ylabel('Oy')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=480)
        plt.close()

        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="heatmap.png"'
        return response

class GraphOneYear(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.POST.get('data'):
            return JsonResponse({'success': 'error', 'message': 'Empty data'})
        
        df = pd.DataFrame(json.loads(request.POST.get('data')))
        year = request.POST.get('year')
        well_id = request.POST.get('well_id')

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
        title = f'Suv sathi {str(Well.objects.filter(id=well_id).first().well_number) + " - " if well_id else ""}{year_to_plot} yil'
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
        well_id = request.POST.get('well_id')
        
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
        title = f'Suv sathi {str(Well.objects.filter(id=well_id).first().well_number) + " - " if well_id else ""}{year1} yil va {year2} yil'
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


class PasportView(LoginRequiredMixin, TemplateView):
    form_class = PasportForm
    template_name = os.path.join(TEMPLATE_DIR, 'pasport.html')
    
    def post(self, request, *args, **kwargs):
        well_id = request.POST.get('well_id')
        try:
            well_id = int(well_id)
        except:
            return JsonResponse({'success': False, 'message': 'Not Int entered as ID'})
        
        well = Well.objects.get(pk=well_id)
        
        if well:
            coordinate = well.coordinates.first()
            well_data = {
                "id": well.id,
                "organization": well.organization.name,
                "well_number": well.well_number,
                "expedicion": well.expedicion.name,
                "type": well.type.name,
                "region":well.region.name,
                "district": well.district.name,
                "address": well.address,
                "location": well.location.name,
                "created_at": well.created_at.strftime("%Y-%m-%d"),
                
                "coordinate": {
                    "lat_degree": coordinate.lat_degree,
                    "lat_minute": coordinate.lat_minute,
                    "lat_second": coordinate.lat_second,
                    "lon_degree": coordinate.lon_degree,
                    "lon_minute": coordinate.lon_minute,
                    "lon_second": coordinate.lon_second,
                    "x": coordinate.x,
                    "y": coordinate.y
                } if coordinate else ''
            }
            
            return JsonResponse({'success': True, 'well':well_data})
        else:
            return JsonResponse({'success': False, 'message': 'Not such well'})
    
