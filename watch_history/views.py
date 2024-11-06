from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from content.models import Video
from watch_history.models import WatchHistory


class UpdateWatchHistory(APIView):
    def post(self, request):
        user = request.user
        video_id = request.data.get("video_id")
        timestamp = request.data.get("timestamp")

        if not video_id or timestamp is None:
            return Response(
                {"error": "Video ID and timestamp are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        video = Video.objects.get(id=video_id)
        watch_history, created = WatchHistory.objects.get_or_create(
            user=user, video=video
        )
        watch_history.timestamp = timestamp
        watch_history.save()

        return Response({"message": "Watch history updated"}, status=status.HTTP_200_OK)


class GetWatchHistory(APIView):
    def get(self, request):
        user = request.user
        watch_history = WatchHistory.objects.filter(user=user).select_related("video")
        data = [
            {
                "video_id": entry.video.id,
                "title": entry.video.title,
                "timestamp": entry.timestamp,
                "last_watched": entry.last_watched,
            }
            for entry in watch_history
        ]
        return Response(data, status=status.HTTP_200_OK)
