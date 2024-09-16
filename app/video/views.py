from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .serializers import VideoUploadSerializer, CategorySerializer
from rest_framework import permissions, viewsets, mixins
from keycloakAuth.keycloakAuth.authentication import (
    KeycloakAuthentication,
    IsKeycloakAuthenticated
)
from .models import Video, Category
from core.pagination import CustomPageNumberPagination
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class VideoUploadView(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = VideoUploadSerializer
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [IsKeycloakAuthenticated]
    queryset = Video.objects.all()
    pagination_class = CustomPageNumberPagination
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        file = self.request.data['video']
        # Save video instance
        video = serializer.save(
            created_by=self.request.user.sub,
        )

        # Example progress update
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'progress_group',
            {
                'type': 'send_progress',
                'progress': 50  # Example progress
            }
        )
        return video


class CategoryView(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet
                   ):
    serializer_class = CategorySerializer
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [IsKeycloakAuthenticated]
    queryset = Category.objects.all()

    def get_permissions(self):
        """Allow unauthenticated access to GET requests."""
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


def upload_page(request):
    return render(request, 'video_upload.html')
