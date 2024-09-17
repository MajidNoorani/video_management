from .serializers import (
    # UploadFileSerializer,
    CategorySerializer,
    VideoSerializer
)
from rest_framework import permissions, viewsets, mixins
from keycloakAuth.keycloakAuth.authentication import (
    KeycloakAuthentication,
    IsKeycloakAuthenticated
)
from .models import Video, Category
from core.pagination import CustomPageNumberPagination
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .exceptions import CustomAccessException
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)
from datetime import timedelta


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'category',
                OpenApiTypes.INT,
                description="ID of the desired category.",
            ),
            OpenApiParameter(
                'min_duration',
                OpenApiTypes.STR,
                description='Minimum duration. (HH:MM:SS)',
            ),
            OpenApiParameter(
                'max_duration',
                OpenApiTypes.STR,
                description='Maimum duration. (HH:MM:SS)',
            )
        ]
    )
)
@method_decorator(csrf_exempt, name='dispatch')
class VideoUploadView(viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    serializer_class = VideoSerializer
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [IsKeycloakAuthenticated]
    queryset = Video.objects.all()
    pagination_class = CustomPageNumberPagination
    # parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get filters from the query params
        category_id = self.request.query_params.get('category')
        min_duration_str = self.request.query_params.get('min_duration')
        max_duration_str = self.request.query_params.get('max_duration')

        # Apply filter for category_id
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        # Apply filter for min_duration and max_duration
        if min_duration_str or max_duration_str:
            try:
                if min_duration_str:
                    min_hours, min_minutes, min_seconds = \
                        map(int, min_duration_str.split(':'))
                    min_duration \
                        = timedelta(hours=min_hours,
                                    minutes=min_minutes,
                                    seconds=min_seconds)
                    queryset = queryset.filter(duration__gte=min_duration)

                if max_duration_str:
                    max_hours, max_minutes, max_seconds = \
                        map(int, max_duration_str.split(':'))
                    max_duration = \
                        timedelta(hours=max_hours,
                                  minutes=max_minutes,
                                  seconds=max_seconds)
                    queryset = queryset.filter(duration__lte=max_duration)

            except ValueError:
                pass  # Handle invalid format if needed

        return queryset

    def perform_create(self, serializer):
        file = self.request.data['video']
        total_size = file.size
        chunk_size = 8192  # 8KB chunks
        uploaded_size = 0

        # Save video instance
        video = serializer.save(
            created_by=self.request.user.sub,
        )

        channel_layer = get_channel_layer()

        while uploaded_size < total_size:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            uploaded_size += len(chunk)
            progress = int((uploaded_size / total_size) * 100)

            # Send progress update
            async_to_sync(channel_layer.group_send)(
                'progress_group',
                {
                    'type': 'send_progress',
                    'progress': progress
                }
            )

        return video


class CategoryView(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
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
        if self.request.user.is_admin():
            serializer.save(
                created_by=self.request.user.sub,
                updated_by=self.request.user.sub)
        else:
            raise CustomAccessException(
                    message="Only admin users are allowed to create a category"
                )

    def perform_update(self, serializer):
        if self.request.user.is_admin():
            serializer.save(
                updated_by=self.request.user.sub,
                updated_date=timezone.now()
            )
        else:
            raise CustomAccessException(
                    message="Only admin users are allowed to update a category"
                )

    def perform_destroy(self, instance):
        if self.request.user.is_admin():
            instance.delete()
        else:
            raise CustomAccessException(
                message="Only admin users are allowed to delete a category"
            )


def upload_page(request):
    return render(request, 'video_upload.html')
