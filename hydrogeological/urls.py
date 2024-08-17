from . import views
from . import shows
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('pasport/', views.PasportView.as_view(), name='pasport'),
    path('water-level/', views.GroundWaterLevelView.as_view(), name='water-level'),
    path('water-chemic/', views.GroundWaterChemicalView.as_view(), name='water-chemic'),
    path('station/', views.station, name='station'),
    path('well/', views.well, name='station'),
    path('import/', views.ImportView.as_view(), name='import'),
    path('station-well/', views.station_well, name='station-well'),
    
    path('show/', shows.HomeView.as_view(), name='home-show'),
    path('show/pasport/', shows.PasportView.as_view(), name='pasport-show'),
    path('show/water-level/', shows.GroundWaterLevelView.as_view(), name='water-level-show'),
    path('show/water-level/heatmap', shows.HeatMap.as_view(), name='water-level-heatmap'),
    path('show/water-level/one-year', shows.GraphOneYear.as_view(), name='water-level-one-year'),
    path('show/water-level/compare-year', shows.GraphCompareTwoYears.as_view(), name='water-level-compare-year'),
    
    path('lithologic/', views.LithologicView.as_view(), name='lithologic'),
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)