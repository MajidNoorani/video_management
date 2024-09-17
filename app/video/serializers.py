from rest_framework import serializers
from .models import Video, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=True)

    class Meta:
        model = Video
        fields = ['id', 'video', 'title', 'description',
                  'duration', 'category']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(
            instance.category.all(),
            many=True).data
        return representation

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        video = Video.objects.create(**validated_data)
        video.category.set(categories)
        return video

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', None)
        instance = super().update(instance, validated_data)
        if categories is not None:
            instance.category.set(categories)
        return instance
