import pandas as pd
import numpy as np
import json
import copy
from django.http import JsonResponse
from django.apps import apps
from pymannkendall import original_test as mk_test

# Helper function to fetch data from a model based on dynamic filtering
def fetch_data(app_name, model_name, filter_field, filter_value):
    model = apps.get_model(app_label=app_name, model_name=model_name)
    filter_kwargs = {f"{filter_field}": filter_value}
    
    data = model.objects.filter(**filter_kwargs).values(
        'year', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'
    )
    
    if not data:
        return None, {'status': 'error', 'message': 'No data found for the specified filters'}
    
    return pd.DataFrame(list(data)), None

# Helper function to clean and sort data
def clean_and_sort_data(df, start_year=None, end_year=None, start_month=1, end_month=12):
    df['year'] = df['year'].astype(str)
    df = df.sort_values(by='year', ascending=True)

    year_min = int(df['year'].min())
    year_max = int(df['year'].max())
    
    start_year = start_year or year_min
    end_year = end_year or year_max
    
    start_month = start_month or 1
    end_month = end_month or 12
    
    month_mapping = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 
                     7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'}
    
    for index, row in df.iterrows():
        if row['year'] < str(start_year) or row['year'] > str(end_year):
            df.drop(index, inplace=True)
        if row['year'] == str(start_year):
            for month in range(1, 13):
                if month < int(start_month):
                    column_name = month_mapping[month]
                    df.at[index, column_name] = np.nan
        if row['year'] == str(end_year):
            for month in range(1, 13):
                if month > int(end_month):
                    column_name = month_mapping[month]
                    df.at[index, column_name] = np.nan

    return df

# Helper function to calculate statistics
def calculate_statistics(df):
    df['yearly_avg'] = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean(axis=1)
    df['amplitude'] = df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].max(axis=1) - df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].min(axis=1)

    mk_results = {}
    for metric in ['Tau', 'p', 'h', 's', 'var_s']:
        try:
            mk_results[metric] = {month: getattr(mk_test(df[month]), metric) for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}
        except ZeroDivisionError:
            mk_results[metric] = {month: None for month in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']}

    stats = {
        'Variance': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].var().to_dict(),
        'Standard Deviation': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].std().to_dict()
    }

    overall_avg = df[['yearly_avg']].mean().values[0]
    cv = {month: str(round((std / overall_avg) * 100, 2)) + '%' if std else None for month, std in stats['Standard Deviation'].items()}

    return stats, mk_results, cv

# Main function to process request and return data
def process_request(app_name, model_name, filter_field, filter_value, start_year=None, end_year=None, start_month=1, end_month=12):
    df, error = fetch_data(app_name, model_name, filter_field, filter_value)
    if error:
        return error

    df = clean_and_sort_data(df, start_year, end_year, start_month, end_month)
    filtered_df = copy.deepcopy(df)
    stats, mk_results, cv = calculate_statistics(df)

    variance_row = {'year': 'Variance', **stats['Variance']}
    std_dev_row = {'year': 'Standard Deviation', **stats['Standard Deviation']}
    cv_row = {'year': 'Coefficient of Variation', **cv}
    
    variance_row_df = pd.DataFrame([variance_row])
    std_dev_row_df = pd.DataFrame([std_dev_row])
    cv_row_df = pd.DataFrame([cv_row])
    mk_rows = [pd.DataFrame([{**{'year': metric}, **values}]) for metric, values in mk_results.items()]
    
    # Combine dataframes with stats and Mann-Kendall test results
    
    all_time_stats = {
        'min': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].min().min(),
        'max': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].max().max(),
        'avg': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean().mean(),
        'variance': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].var().var(),
        'std_dev': df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].std().std(),
        'cv': str(round((df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].std().std() / 
                          df[['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']].mean().mean() * 100), 2)) + '%'
    }
    
    start_year = start_year or int(df['year'].min())
    start_month = start_month or 1
    end_year = end_year or int(df['year'].max())
    end_month = end_month or 12
    
    df = pd.concat([df, variance_row_df, std_dev_row_df, cv_row_df, *mk_rows], ignore_index=True)

    return {
        'success': True,
        'data': json.loads(df.to_json(orient='records')),
        'start_year': start_year,
        'end_year': end_year,
        'start_month': start_month,
        'end_month': end_month,
        'all_time_min': all_time_stats['min'],
        'all_time_max': all_time_stats['max'],
        'all_time_avg': round(all_time_stats['avg'], 2),
        'all_time_variance': round(all_time_stats['variance'], 2),
        'all_time_std_dev': round(all_time_stats['std_dev'], 2),
        'all_time_cv': all_time_stats['cv'],
        'filtered_df': json.loads(filtered_df.to_json(orient='records'))
    }
