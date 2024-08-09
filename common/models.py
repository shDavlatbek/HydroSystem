from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Region(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Viloyat'
        verbose_name_plural = 'Viloyat'

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tuman'
        verbose_name_plural = 'Tuman'
    
# with open(file_path, 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     for line in lines:
#         line = line.strip()
#         if line:  
#             obj, created = Location.objects.get_or_create(name=line)