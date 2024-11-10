from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.response import Response
from rest_framework.views import APIView
from content.functions import (
    get_category_videos,
    get_latest_video,
    get_latest_views,
    get_my_videos,
    get_selected_video,
    get_video,
)
from content.models import Video
from rest_framework import status

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class DashboardView(APIView):
    def get(self, request):
        """
        This function returns the data for the dashboard. It gets the 6 latest videos, the videos the user has watched, all the categories and the videos sorted by categories.
        """
        try:
            latest_videos = get_latest_views()
            my_videos = get_my_videos(request)
            categories = Video.objects.values_list("category", flat=True).distinct()
            category_videos = get_category_videos(categories)

            return Response(
                {
                    "latest_videos": latest_videos,
                    "my_videos": my_videos,
                    "category_videos": category_videos,
                    "categories": categories,
                }
            )
        except Exception as e:
            return Response(
                {
                    "error": f"An error occurred while loading the dashboard data. {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class HeroView(APIView):
    def get(self, request):
        """
        This function returns the data for the hero area. If the user is new on the page, the latest video is returned, else the selected video.
        """
        video_id = request.query_params.get("id")

        if video_id == "-1":
            latest_video = get_latest_video()
            return Response(latest_video, status=status.HTTP_200_OK)

        else:
            try:
                video = get_selected_video(video_id)
                return Response(video, status=status.HTTP_200_OK)
            except Video.DoesNotExist:
                return Response(
                    {"message": "Video not found"}, status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {
                        "message": f"An error occurred while loading hero video data. {str(e)}"
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


@method_decorator(cache_page(CACHE_TTL), name="dispatch")
class VideoView(APIView):
    def get(self, request):
        """
        This function returns the video data for the actual video the user wants to watch. It returns the m3u8 file based on the given resolution.
        """
        video_id = request.query_params.get("id")
        user = request.user
        resolution = request.query_params.get("resolution")

        try:
            video = get_video(video_id, user, resolution)
            return Response(video, status=status.HTTP_200_OK)

        except Video.DoesNotExist:
            return Response(
                {"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": f"An error occurred while loading video data. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
