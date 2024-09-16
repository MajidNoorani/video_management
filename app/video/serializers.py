from rest_framework import serializers
from .models import Video, Category


class VideoUploadSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
        )

    class Meta:
        model = Video
        fields = ['video', 'title', 'description',
                  'duration', 'category']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Category with this name already exists."
                )
        return value
