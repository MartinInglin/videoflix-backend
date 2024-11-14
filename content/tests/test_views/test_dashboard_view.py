from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from authentication.models import CustomUser
from content.models import Video
from content.serializers import DashboardVideoSerializer
from watch_history.models import WatchHistory
from freezegun import freeze_time
from unittest.mock import patch


class DashboardViewTests(APITestCase):

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
            serialized_video = DashboardVideoSerializer(video)
            self.categorized_videos[category].append(serialized_video.data)

        self.watch_history = WatchHistory.objects.create(
            user=self.user, video=self.videos[0], timestamp=0
        )

        self.latest_videos = [
            DashboardVideoSerializer(video).data for video in self.videos[4:][::-1]
        ]

        self.my_videos = [
            DashboardVideoSerializer(video).data for video in self.videos[:1]
        ]

    def test_get_dashboard_data(self):
        url = reverse("dashboard")

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["latest_videos"], self.latest_videos)
        self.assertEqual(response.data["my_videos"], self.my_videos)
        self.assertCountEqual(response.data["categories"], self.categories)
        self.assertEqual(response.data["category_videos"], self.categorized_videos)

    # @patch(
    #     "content.functions.get_latest_videos",
    #     side_effect=Exception("Get latest videos failed"),
    # )
    # def test_get_latest_videos_fails(self, mock_get_videos):
    #     url = reverse("dashboard")

    #     response = self.client.get(url, format="json")

    #     self.assertEqual(mock_get_videos.called, True)

    #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def test_get_my_videos_fails(self):
    #     pass

    # def test_get_categories_fails(self):
    #     pass

    # def test_get_category_videos_fails(self):
    #     pass

    def test_invalid_token(self):
        self.token = "123456"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        url = reverse("dashboard")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
