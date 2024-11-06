from rest_framework import serializers
from .models import Video

class DashboardVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'created_at', 'category', 'thumbnail']


class HeroVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'teaser']