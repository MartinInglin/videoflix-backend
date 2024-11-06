from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.response import Response
from rest_framework.views import APIView
from content.models import Video
from content.serializers import DashboardVideoSerializer, HeroVideoSerializer
from rest_framework import status

from watch_history.models import WatchHistory

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class DashboardView(APIView):
    def get(self, request):
        latest_videos = Video.objects.order_by("-created_at")[:6]
        latest_videos_serialized = DashboardVideoSerializer(
            latest_videos, many=True
        ).data

        watch_history = WatchHistory.objects.filter(user=request.user).select_related("video")
        video_ids = watch_history.values_list("video__id", flat=True)
        my_videos = Video.objects.filter(id__in=video_ids)
        my_videos_serialized = DashboardVideoSerializer(my_videos, many=True).data

        categories = Video.objects.values_list("category", flat=True).distinct()
        category_videos = {}
        for category in categories:
            videos = Video.objects.filter(category=category)
            category_videos[category] = DashboardVideoSerializer(videos, many=True).data

        return Response(
            {
                "latest_videos": latest_videos_serialized,
                "my_videos": my_videos_serialized,
                "category_videos": category_videos,
                "categories": categories,
            }
        )


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class HeroView(APIView):
    def get(self, request):
        video_id = request.query_params.get("id")

        if video_id=='-1':
            latest_video = Video.objects.order_by('created_at').first()
            video = latest_video
            serializer = HeroVideoSerializer(video)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:

            try:
                video = Video.objects.get(id=video_id)
                serializer = HeroVideoSerializer(video)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Video.DoesNotExist:
                return Response(
                    {"message": "Video not found"}, status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"message": f"Something went wrong: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
