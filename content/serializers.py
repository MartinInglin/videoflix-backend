from rest_framework import serializers
from .models import Video

class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'category', 'thumbnail']