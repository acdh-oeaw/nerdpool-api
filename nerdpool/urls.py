from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from archiv import api_views

router = routers.DefaultRouter()
router.register(r'ner-source', api_views.NerSourceViewSet)
router.register(r'ner-sample', api_views.NerSampleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', include('archiv.urls')),
    path('admin/', admin.site.urls),
]
