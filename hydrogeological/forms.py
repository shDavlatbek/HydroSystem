import datetime
from django import forms 
from hydrogeological.models import Well, Coordinate, WaterLevel



class PasportForm(forms.ModelForm):
    
    lat_degree = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    lat_minute = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    lat_second = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    lon_degree = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    lon_minute = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    lon_second = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    x = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    y = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    
    created_at = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format="%Y-%m-%d", 
            attrs={
                'class': 'form-control', 
                'type': 'date',
                'value': datetime.datetime.now().strftime("%Y-%m-%d")
                }
        ),
        input_formats=["%Y-%m-%d"]
    )
    
    class Meta:
        model = Well
        fields = [
            'organization', 'well_number', 'station', 'type', 'region', 'district', 'address', 'location', 'created_at',
            'lat_degree', 'lat_minute', 'lat_second', 'lon_degree', 'lon_minute', 'lon_second', 'x', 'y'
            ]
    
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-control', 'required':'required'}),
            'well_number': forms.NumberInput(attrs={'class': 'form-control', 'required':'required'}),
            'station': forms.Select(attrs={'class': 'form-control', 'required':'required'}),
            'type': forms.Select(attrs={'class': 'form-control', 'required':'required'}),
            'region': forms.Select(attrs={'class': 'form-control region_select', 'required':'required'}),
            'district': forms.Select(attrs={'class': 'form-control district_select', 'required':'required'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required':'required'}),
            'location': forms.Select(attrs={'class': 'form-control', 'required':'required'}),
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'required':'required'}),
        }
    
    def save(self, commit=True):
        well_instance = super().save(commit=False)
        if commit:
            well_instance.save()
        
        coordinate_data = {
            'lat_degree': self.cleaned_data.get('lat_degree'),
            'lat_minute': self.cleaned_data.get('lat_minute'),
            'lat_second': self.cleaned_data.get('lat_second'),
            'lon_degree': self.cleaned_data.get('lon_degree'),
            'lon_minute': self.cleaned_data.get('lon_minute'),
            'lon_second': self.cleaned_data.get('lon_second'),
            'x': self.cleaned_data.get('x'),
            'y': self.cleaned_data.get('y'),
            'well': well_instance
        }
        
        Coordinate.objects.create(**coordinate_data)
        
        return well_instance
    
class WaterLevelForm(forms.ModelForm):
    well = forms.ModelChoiceField(
        queryset=Well.objects.all()
    )
    class Meta:
        model = WaterLevel
        fields = '__all__'