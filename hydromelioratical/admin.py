from django.contrib import admin
from .models import *

class CoordinateInline(admin.TabularInline):
    model = Coordinate
    max_num = 1
    extra = 0 # Number of extra forms to display

class WaterLevelInline(admin.TabularInline):
    model = WaterLevel
    extra = 0

@admin.register(Well)
class WellAdmin(admin.ModelAdmin):
    inlines = [CoordinateInline, WaterLevelInline]
