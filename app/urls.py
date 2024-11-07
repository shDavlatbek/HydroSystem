from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("table/", views.TableView.as_view(), name="table"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('hydropost/', HydropostView.as_view(), name='hydropost'),
    path('hydropost-mode/', HydropostModeView.as_view(), name='hydropost-mode'),
    path("meteostation/", MeteostationView.as_view(), name="meteostation"),
    path("meteostation-parameter/", MeteostationParameterView.as_view(), name="meteostation-parameter"),
    path("import/", ImportView.as_view(), name="import")
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)