from content.models import Video
from content.serializers import (
    DashboardVideoSerializer,
    HeroVideoSerializer,
    VideoSerializer,
)
from watch_history.models import WatchHistory


def get_latest_views():
    latest_videos = Video.objects.order_by("-created_at")[:6]
    latest_videos_serialized = DashboardVideoSerializer(latest_videos, many=True).data
    return latest_videos_serialized


def get_my_videos(request):
    watch_history = WatchHistory.objects.filter(user=request.user).select_related(
        "video"
    )
    video_ids = watch_history.values_list("video__id", flat=True)
    my_videos = Video.objects.filter(id__in=video_ids)
    my_videos_serialized = DashboardVideoSerializer(my_videos, many=True).data
    return my_videos_serialized


def get_category_videos(categories):
    category_videos = {}
    for category in categories:
        videos = Video.objects.filter(category=category)
        category_videos[category] = DashboardVideoSerializer(videos, many=True).data
    return category_videos


def get_latest_video():
    latest_video = Video.objects.order_by("created_at").first()
    video = latest_video
    serializer = HeroVideoSerializer(video)
    return serializer.data


def get_selected_video(video_id):
    video = Video.objects.get(id=video_id)
    serializer = HeroVideoSerializer(video)
    return serializer.data


def get_video(video_id, user, resolution):
    video = Video.objects.get(id=video_id)
    serializer = VideoSerializer(
        video, context={"user": user, "resolution": resolution}
    )
    return serializer.data
