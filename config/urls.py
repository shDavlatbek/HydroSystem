from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'), name='index'),
    path("common/", include(("common.urls", "common"), namespace="common")),
    path('hydrogeological/', include(('hydrogeological.urls', 'hydrogeological'), namespace='hydrogeological'), name='hydrogeological'),
    path('hydromelioratical/', include(('hydromelioratical.urls', 'hydromelioratical'), namespace='hydromelioratical'), name='hydromelioratical'),
    path('hydrometeorological/', include(('hydrometeorological.urls', 'hydrometeorological'), namespace='hydrometeorological'), name='hydrometeorological'),
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)