from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('hydrometria/', views.HydrometriaView.as_view(), name='hydrometria'),
    path('meteorology/', views.MeteorologyView.as_view(), name='meteorology'),
    path('show/hydropost-levels/', views.HydrometriaShowView.as_view(), name='hydropost-show'),
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)