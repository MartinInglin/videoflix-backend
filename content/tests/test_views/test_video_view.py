from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from authentication.models import CustomUser
from content.models import Video
from content.serializers import DashboardVideoSerializer, HeroVideoSerializer, VideoSerializer
from watch_history.models import WatchHistory
from freezegun import freeze_time
from unittest.mock import patch
from django.test import override_settings


@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
)
class HeroViewTests(APITestCase):

    @freeze_time("2023-01-01 12:00:00")
    def setUp(self):
        self.user, created = CustomUser.objects.get_or_create(
            username="testuser", password="test1234"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.categories = ["drama", "action", "documentary"]

        self.videos = []
        for i in range(10):
            with freeze_time(f"2023-01-{i + 1:02d} 14:00:00"):
                video = Video.objects.create(
                    id=i + 1,
                    title=f"Test Video {i + 1}",
                    description=f"A test video description {i + 1}",
                    category=self.categories[i % len(self.categories)],
                    thumbnail=f"thumbnail.jpg",
                    teaser=f"teaser.mp4",
                    video_file=f"video.mp4",
                )
                self.videos.append(video)

        self.categorized_videos = {"drama": [], "action": [], "documentary": []}

        for i, video in enumerate(self.videos):
            category = self.categories[i % len(self.categories)]
            video.category = category
            serialized_video = VideoSerializer(video)
            self.categorized_videos[category].append(serialized_video.data)

        self.video = VideoSerializer(self.videos[2]).data

    def test_get_video(self):
        video_id = 3
        resolution = 360
        url = reverse("video")
        url_with_query = f"{url}?id={video_id}&resolution={resolution}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.video)

    def test_id_not_existing(self):
        video_id = 100
        resolution = 360
        url = reverse("video")
        url_with_query = f"{url}?id={video_id}&resolution={resolution}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_video_no_id(self):
        resolution = 360
        url = reverse("video")
        url_with_query = f"{url}?resolution={resolution}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_video_no_resolution(self):
        video_id = 1
        url = reverse("video")
        url_with_query = f"{url}?id={video_id}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resolution_not_existing(self):
        video_id = 100
        resolution = 1
        url = reverse("video")
        url_with_query = f"{url}?id={video_id}&resolution={resolution}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_token(self):
        self.token = "123456"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        hero_id = 1
        url = reverse("video")
        url_with_query = f"{url}?id={hero_id}"

        response = self.client.post(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch(
        "content.views.get_video",
        side_effect=Exception("Get video failed"),
    )
    def test_get_selected_video_fails(self, mock_get_video):
        video_id = 3
        resolution = 360
        url = reverse("video")
        url_with_query = f"{url}?id={video_id}&resolution={resolution}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
