from django.db import models
from common.models import Region

# Create your models here.
class ObjectType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Mode(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.name)
    
class Hydropost(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Gidropost'
        verbose_name_plural = 'Gidropostlar'

class HydropostValue(models.Model):
    hydropost = models.ForeignKey(Hydropost, on_delete=models.CASCADE, related_name='hydropost_values', verbose_name='Gidropost nomi')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='hydropost_values', null=True, verbose_name='Viloyat')
    object_type = models.ForeignKey(ObjectType, on_delete=models.SET_NULL, related_name='hydropost_values', null=True, verbose_name="Suv ob'ekti turi"),
    mode = models.ForeignKey(Mode, on_delete=models.SET_NULL, related_name='hydropost_values', null=True, verbose_name='Rejim turi')
    
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hydropost.name + ' - ' + str(self.mode) + ' - ' + str(self.year)
    
    class Meta:
        verbose_name = 'Gidrometriya'
        verbose_name_plural = 'Gidrometriya'
    
class Meteostation(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Meteostansiya'
        verbose_name_plural = 'Meteostansiyalar'
    
class Parameter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class MeteostationValue(models.Model):
    meteostation = models.ForeignKey(Meteostation, on_delete=models.CASCADE, related_name='meteostation_values')
    parameter = models.ForeignKey(Parameter, on_delete=models.SET_NULL, related_name='meteostation_values', null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='meteostation_values', null=True)

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.meteostation.name + ' - ' + str(self.parameter) + ' - ' + str(self.year)
    
    class Meta:
        verbose_name = 'Meteorologiya'
        verbose_name_plural = 'Meteorologiya'