from django.db import models
from common.models import Location, Region, District

class Organization(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Expedicion(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='expedicions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WellType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Well(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name='melio_wells', null=True, blank=True)
    well_number = models.IntegerField()
    expedicion = models.ForeignKey(Expedicion, on_delete=models.SET_NULL, related_name='melio_wells', null=True, blank=True)
    type = models.ForeignKey(WellType, on_delete=models.SET_NULL, related_name='melio_wells', null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='melio_wells', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, related_name='melio_wells', null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='objects', null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.well_number)

class Coordinate(models.Model):
    well = models.ForeignKey(Well, on_delete=models.CASCADE, related_name='coordinates')
    lat_degree = models.IntegerField(blank=True, null=True)
    lat_minute = models.IntegerField(blank=True, null=True)
    lat_second = models.FloatField(blank=True, null=True)
    lon_degree = models.IntegerField(blank=True, null=True)
    lon_minute = models.IntegerField(blank=True, null=True)
    lon_second = models.FloatField(blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return str(self.well.well_number)
    
    def latitude(self):
        return self.lat_degree + "°" + self.lat_minute / 60 + "'" + self.lat_second / 3600 + '"'
    
    def longitude(self):
        return self.lon_degree + "°" + self.lon_minute / 60 + "'" + self.lon_second / 3600 + '"'
    
class WaterLevel(models.Model):
    well = models.ForeignKey(Well, on_delete=models.CASCADE, related_name='water_levels')
    year = models.IntegerField(verbose_name='Yil')
    I = models.FloatField(blank=True, null=True, verbose_name='Yanvar')
    II = models.FloatField(blank=True, null=True, verbose_name='Fevral')
    III = models.FloatField(blank=True, null=True, verbose_name='Mart')
    IV = models.FloatField(blank=True, null=True, verbose_name='Aprel')
    V = models.FloatField(blank=True, null=True, verbose_name='May')
    VI = models.FloatField(blank=True, null=True, verbose_name='Iyun')
    VII = models.FloatField(blank=True, null=True, verbose_name='Iyul')
    VIII = models.FloatField(blank=True, null=True, verbose_name='Avgust')
    IX = models.FloatField(blank=True, null=True, verbose_name='Sentyabr')
    X = models.FloatField(blank=True, null=True, verbose_name='Oktyabr')
    XI = models.FloatField(blank=True, null=True, verbose_name='Noyabr')
    XII = models.FloatField(blank=True, null=True, verbose_name='Dekabr')
    
    def __str__(self):
        return f'{str(self.well)} - {self.year}'
    