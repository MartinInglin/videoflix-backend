from rest_framework import serializers

from watch_history.models import WatchHistory
from .models import Video


class DashboardVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "created_at", "category", "thumbnail"]


class HeroVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "title", "description", "teaser"]


class VideoSerializer(serializers.ModelSerializer):
    hls_file = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ["id", "title", "hls_file", "timestamp"]

    def get_hls_file(self, obj):
        """
        This function the HLS file depending on the given resolution.
        """
        resolution = self.context.get("resolution", "360")

        hls_field_mapping = {
            "360": obj.hls_file_360,
            "480": obj.hls_file_480,
            "720": obj.hls_file_720,
            "1080": obj.hls_file_1080,
        }

        selected_file = hls_field_mapping.get(resolution)
        return selected_file.url if selected_file else None

    def get_timestamp(self, obj):
        """
        This function gets the timestamp of the video based on the video and the user. If there is no timestamp the function returns 0.
        """
        user = self.context.get("user")

        try:
            watch_history = WatchHistory.objects.get(user=user, video=obj)
            return watch_history.timestamp
        except WatchHistory.DoesNotExist:
            return 0
