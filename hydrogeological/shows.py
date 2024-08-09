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
from .forms import PasportForm, WaterLevelForm
from .models import *
import tempfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import time

TEMPLATE_DIR = str(os.path.join('hydrogeological', 'show'))
URL_NAME = 'hydrogeological'

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'home.html')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buttons'] = [
            {'text':"Kuzatuv-burg'u qudug'i pasporti",'url':f'{URL_NAME}:pasport-show'},
            {'text':"Yerosti suvlari sathi rejimi",'url':f'{URL_NAME}:water-level-show'},
            # {'text':"Yerosti suvlari kimyoviy tarkibi",'url':f'{URL_NAME}:water-chemic'},
        ]
        return context

class GroundWaterLevelView( TemplateView):
    template_name = os.path.join(TEMPLATE_DIR, 'ground_water_level.html')
    
    def post(self, request, *args, **kwargs):
        well_id = request.POST.get('well_id')
        
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        start_month = request.POST.get('start_month')
        end_month = request.POST.get('end_month')
        
        try: well_id = int(well_id)
        except: return JsonResponse({'status': 'error', 'message': 'Invalid well ID'})

        if water_levels := WaterLevel.objects.filter(well__id=well_id).values(
            'year', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'
        ): pass
        else: return JsonResponse({'status': 'error', 'message': 'No data found for the specified well'})
        
        df = pd.DataFrame(list(water_levels))
        
        df['year'] = df['year'].astype(str)
        df = df.sort_values(by='year', ascending=True)
        
        year_max = int(df['year'].max())
        year_min = int(df['year'].min())
        
        if start_year: 
            try: start_year = int(start_year)
            except: start_year = year_min
        else: start_year = year_min
        
        if end_year:
            try: end_year = int(end_year)
            except: end_year = year_max
        else: end_year = year_max
        
        if start_month:
            try: start_month = int(start_month)
            except: start_month = 1
        else: start_month = 1
        
        if end_month:
            try: end_month = int(end_month)
            except: end_month = 12 
        else: end_month = 12
        
        water_levels = WaterLevel.objects.filter(
            well__id=well_id,
            year__range=(start_year, end_year)
        ).values(
            'year', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'
        )
        
        df = pd.DataFrame(list(water_levels))
        
        df['year'] = df['year'].astype(str)
        df = df.sort_values(by='year', ascending=True)
        
        month_mapping = {
            1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 
            7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
        }
        for index, row in df.iterrows():
            if row['year'] == str(start_year):
                for month in range(1, 13):
                    if month < start_month:
                        column_name = month_mapping[month]
                        df.at[index, column_name] = np.nan
            
            if row['year'] == str(end_year):
                for month in range(1, 13):
                    if month > end_month:
                        column_name = month_mapping[month]
                        df.at[index, column_name] = np.nan
        
        filtered_df = copy.deepcopy(df)

        df['yearly_avg'] = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean(axis=1)
        df['amplitude'] = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].max(axis=1) - df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].min(axis=1)
        
        
        ''' MAN KELLDALL '''
        try:
            mk_tau = {month: mk.original_test(df[month]).Tau for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        except ZeroDivisionError:
            mk_tau = {month: None for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        mk_tau_row = {'year': 'Tau', **mk_tau}
        
        try:
            mk_p = {month: mk.original_test(df[month]).p for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        except ZeroDivisionError:
            mk_p = {month: None for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        mk_p_row = {'year': 'P-value', **mk_p}
        
        try:
            mk_h = {month: mk.original_test(df[month]).h for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        except ZeroDivisionError:
            mk_h = {month: None for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        mk_h_row = {'year': 'H-value', **mk_h}
        
        try:
            mk_s = {month: mk.original_test(df[month]).s for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        except ZeroDivisionError:
            mk_s = {month: None for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        mk_s_row = {'year': 'S-value', **mk_s}
        
        try:
            mk_var_s = {month: mk.original_test(df[month]).var_s for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        except ZeroDivisionError:
            mk_var_s = {month: None for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        mk_var_s_row = {'year': 'Var-S', **mk_var_s}

        ''' END MAN KELLDALL '''

        statistics = {
            'Variance': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].var().to_dict(),
            'Standard Deviation': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].std().to_dict()
        }

        
        overall_avg = df[['yearly_avg']].mean().values[0] 
        cv = {month: str(round((std / overall_avg) * 100, 2)) + '%' if str(round((std / overall_avg) * 100, 2)) + '%'!='nan%' else None if overall_avg != 0 else None for month, std in statistics['Standard Deviation'].items()}

        variance_row = {'year': 'Variance', **statistics['Variance']}
        std_dev_row = {'year': 'Standard Deviation', **statistics['Standard Deviation']}
        cv_row = {'year': 'Coefficient of Variation', **cv}
        

        variance_row_df = pd.DataFrame([variance_row])
        std_dev_row_df = pd.DataFrame([std_dev_row])
        cv_row_df = pd.DataFrame([cv_row])
        mk_tau_row_df = pd.DataFrame([mk_tau_row])
        mk_p_row_df = pd.DataFrame([mk_p_row])
        mk_h_row_df = pd.DataFrame([mk_h_row])
        mk_s_row_df = pd.DataFrame([mk_s_row])
        mk_var_s_row_df = pd.DataFrame([mk_var_s_row])
        
        monthly_min = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].min().to_dict()
        monthly_max = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].max().to_dict()
        monthly_avg = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean().to_dict()

        monthly_min['year'] = 'Min'
        monthly_max['year'] = 'Max'
        monthly_avg['year'] = 'Avg'

        min_row = pd.DataFrame([monthly_min])
        max_row = pd.DataFrame([monthly_max])
        avg_row = pd.DataFrame([monthly_avg])

        empty_row = pd.DataFrame([{'year': '—————', 'I': '—————', 'II': '—————', 'III': '—————', 'IV': '—————', 'V': '—————', 'VI': '—————', 'VII': '—————', 'VIII': '—————', 'IX': '—————', 'X': '—————', 'XI': '—————', 'XII': '—————', 'yearly_avg': '—————', 'amplitude': '—————'}])

        all_time_min = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].min().min()
        all_time_max = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].max().max()
        all_time_avg:int = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean().mean()
        all_time_variance:int = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].var().var()
        all_time_std_dev:int = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].std().std()
        all_time_cv = str(round((all_time_std_dev / all_time_avg * 100), 2)) + '%' if str(round((all_time_std_dev / all_time_avg * 100), 2)) + '%' != 'nan%' else None if all_time_avg != 0 else None
        
        df = pd.concat([
            df, empty_row, min_row, max_row, avg_row, 
            variance_row_df, std_dev_row_df, cv_row_df,
            mk_tau_row_df, mk_p_row_df, mk_h_row_df, mk_s_row_df, mk_var_s_row_df
            ], ignore_index=True)
        
        return JsonResponse({
            'success': True,
            'data': json.loads(df.to_json(orient='records')),
            # 'image_path': image_path,
            'start_year': start_year,
            'end_year': end_year,
            'start_month': start_month,
            'end_month': end_month,
            'all_time_min': all_time_min,
            'all_time_max': all_time_max,
            'all_time_avg': round(all_time_avg, 2),
            'all_time_variance': round(all_time_variance, 2),
            'all_time_std_dev': round(all_time_std_dev, 2),
            'all_time_cv': all_time_cv,
            'filtered_df': json.loads(filtered_df.to_json(orient='records'))
        })
        
class HeatMap(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.POST.get('data'): return JsonResponse({'success': False, 'message':'Empty data'})
        df = pd.DataFrame(json.loads(request.POST.get('data')))
        
        matplotlib.use('agg')
        plt.figure(figsize=(len(df), 8), dpi=480)
        
        try:
            sns.heatmap(df.set_index('year').T, annot=True, fmt=".1f", cmap="YlOrBr", cbar=True,) # xticklabels=True, yticklabels=True  
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
        if not request.POST.get('data'): return JsonResponse({'success': 'error', 'message':'Empty data'})
        df = pd.DataFrame(json.loads(request.POST.get('data')))
        year = request.POST.get('year')
        well_id = request.POST.get('well_id')
        
        if year not in df['year'].values:
            return JsonResponse({'success': 'error', 'message': 'Year not found'})
        
        matplotlib.use('agg')
        # plt.figure(figsize=(len(df), 8), dpi=480)


        year_to_plot = year
        df_year = df[df['year'] == year_to_plot].drop(columns='year').T  # Drop the 'year' column and transpose
        df_year.columns = [year_to_plot]  # Rename the column to the year

        # Plot the data
        plt.figure(figsize=(12, 6))  # Set the figure size
        plt.plot(df_year, marker='o', linestyle='solid', color='b', label=f'{year_to_plot}')

        # for i, (month, value) in enumerate(df_year[year_to_plot].items()):
        #     plt.text(x=i, y=value, s=f'{value:.1f}', fontsize=9, ha='center', va='bottom', color='black', verticalalignment='bottom')

        for i, (month, value) in enumerate(df_year[year_to_plot].items()):
            plt.annotate(f'{value:.1f}', (i, value), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color='black') 
        
        title = f'Suv sathi {str(Well.objects.filter(id=well_id).first().well_number) + " - "  if well_id else ""}{year_to_plot} yil'
        plt.title(label=title, y=1.05)
        plt.grid()
        plt.xlabel('Oylar')
        plt.ylabel('Sathi')
        
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
            return JsonResponse({'success': 'error', 'message':'Empty data'})
        
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

        # Plot the data
        plt.figure(figsize=(12, 6))  # Set the figure size
        
        plt.plot(df_year1, marker='o', linestyle='solid', color='b', label=f'{year1}')
        plt.plot(df_year2, marker='o', linestyle='solid', color='r', label=f'{year2}')

        for i, (month, value) in enumerate(df_year1[year1].items()):
            plt.annotate(f'{value:.1f}', (i, value), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color='black') 

        for i, (month, value) in enumerate(df_year2[year2].items()):
            plt.annotate(f'{value:.1f}', (i, value), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color='black') 
        
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
                "station": well.station.name,
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
    
