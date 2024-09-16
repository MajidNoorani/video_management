from django.urls import path, include
from rest_framework.routers import DefaultRouter
from video import views
from django.urls import re_path
from video.consumers import ProgressConsumer

router = DefaultRouter()
router.register('video', views.VideoUploadView)
router.register('category', views.CategoryView)

app_name = 'video_Management'

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.upload_page, name='upload_page'),
]

websocket_urlpatterns = [
    re_path(r'ws/upload/$', ProgressConsumer.as_asgi()),
]