from rest_framework import serializers

from .models import ImageUpload


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ("id", "user", "image", "public_id")
        read_only_fields = ("user", "public_id")
