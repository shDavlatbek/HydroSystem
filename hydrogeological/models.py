from django.db import models
from common.models import Location, Region, District

class Organization(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Station(models.Model):
    name = models.CharField(max_length=100)
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
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name='wells', null=True, blank=True, verbose_name="Tashkilot")
    well_number = models.IntegerField(verbose_name="Kuzatuv qudug'i raqami")
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, related_name='wells', null=True, blank=True, verbose_name="Stansiya")
    type = models.ForeignKey(WellType, on_delete=models.SET_NULL, related_name='wells', null=True, blank=True, verbose_name="Qudug'ining turi")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='wells', null=True, blank=True, verbose_name="Viloyat")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, related_name='wells', null=True, blank=True, verbose_name="Tuman")
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Mo'ljal")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='wells', null=True, blank=True, verbose_name="Joylashuv o'rni")
    created_at = models.DateTimeField(verbose_name="To'ldirilgan sanasi")
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.region) + ' - ' + str(self.station) + ' - ' + str(self.well_number)
    
    class Meta:
        verbose_name = "Kuzatuv-burg'u qudug'i"
        verbose_name_plural = "Kuzatuv-burg'u qudug'lari"

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
        return str(self.well)
    
    def latitude(self):
        return self.lat_degree + "°" + self.lat_minute / 60 + "'" + self.lat_second / 3600 + '"'
    
    def longitude(self):
        return self.lon_degree + "°" + self.lon_minute / 60 + "'" + self.lon_second / 3600 + '"'
    
    class Meta:
        verbose_name = 'Koordinat'
        verbose_name_plural = 'Koordinatlar'
    
class WaterLevel(models.Model):
    well = models.ForeignKey(Well, on_delete=models.CASCADE, related_name='water_levels', verbose_name="Kuzatuv qudug'i raqami")
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
        return f'{self.well} - {self.year}'
    
    class Meta:
        verbose_name = "Yerosti suvlari sathi"
        verbose_name_plural = "Yerosti suvlari sathi"