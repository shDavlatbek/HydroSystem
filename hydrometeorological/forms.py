import datetime
from django import forms 
from .models import *
from common.models import Region

class HydrometriaForm(forms.ModelForm):
    
    hydropost = forms.ModelChoiceField(
        queryset=Hydropost.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    object_type = forms.ModelChoiceField(
        queryset=ObjectType.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mode = forms.ModelChoiceField(
        queryset=Mode.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = HydropostValue
        fields = ['I', 'II', 'III', 'IV', 'IX', 'V', 'VI', 'VII', 'VIII', 'X', 'XI', 'XII', 'hydropost', 'mode', 'region', 'year', 'object_type']

class MeteorologyForm(forms.ModelForm):

    meteostation = forms.ModelChoiceField(
        queryset=Meteostation.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    parameter = forms.ModelChoiceField(
        queryset=Parameter.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = MeteostationValue
        fields = ['I', 'II', 'III', 'IV', 'IX', 'V', 'VI', 'VII', 'VIII', 'X', 'XI', 'XII', 'meteostation', 'parameter', 'region', 'year']