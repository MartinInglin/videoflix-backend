from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from authentication.models import CustomUser
from content.models import Video
from content.serializers import HeroVideoSerializer
from freezegun import freeze_time


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
            serialized_video = HeroVideoSerializer(video)
            self.categorized_videos[category].append(serialized_video.data)

        self.latest_video = HeroVideoSerializer(self.videos[-1]).data

    def test_get_latest_hero_video(self):
        hero_id = -1
        url = reverse("hero")
        url_with_query = f"{url}?id={hero_id}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.latest_video)

    def test_get_selected_hero_video(self):
        hero_id = 3
        url = reverse("hero")
        url_with_query = f"{url}?id={hero_id}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 3)

    def test_video_not_existing(self):
        hero_id = 100
        url = reverse("hero")
        url_with_query = f"{url}?id={hero_id}"

        response = self.client.get(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_id(self):
        url = reverse("hero")

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_token(self):
        self.token = "123456"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        hero_id = 1
        url = reverse("hero")
        url_with_query = f"{url}?id={hero_id}"

        response = self.client.post(url_with_query, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
