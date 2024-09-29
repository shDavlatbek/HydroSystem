from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('hydrometria/', views.HydrometriaView.as_view(), name='hydrometria'),
    path('meteorology/', views.MeteorologyView.as_view(), name='meteorology'),
    path('show/hydropost-levels/', views.HydrometriaShowView.as_view(), name='hydropost-show'),
    path('show/hydropost-levels/one-year', views.GraphOneYear.as_view(), name='hydropost-one-year'),
    path('show/hydropost-levels/compare-year', views.GraphCompareTwoYears.as_view(), name='hydropost-compare-year'),
    path('show/meteostation-levels/', views.MeteostationShowView.as_view(), name='meteostation-show'),
    path('show/meteostation-levels/one-year', views.MeteostationGraphOneYear.as_view(), name='meteostation-one-year'),
    path('show/meteostation-levels/compare-year', views.MeteostationGraphCompareTwoYears.as_view(), name='meteostation-compare-year'),
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)