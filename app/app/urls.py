from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from channels.routing import ProtocolTypeRouter, URLRouter
from video.urls import websocket_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'
    ),
    path('api/keycloakAuth/', include('keycloakAuth.keycloakAuth.urls')),
    path('api/video/', include('video.urls')),
]

urlpatterns += [path('i18n/', include('django.conf.urls.i18n'))]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )


application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})
