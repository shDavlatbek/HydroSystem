from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('regions/', views.RegionListView.as_view(), name='region-list'),
    path('districts/', views.DistrictListView.as_view(), name='district-list'),
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)