from rest_framework.test import APITestCase

from content.serializers import HeroVideoSerializer


class HeroVideoSerializerTests(APITestCase):

    def setUp(self):
        self.hero_video_data = {
            "title": "Video title",
            "description": "Video description",
            "teaser": "teaser.mp4",
        }

    def test_contains_expected_fields(self):
        serializer = HeroVideoSerializer(instance=self.hero_video_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(["title", "description", "teaser"]))
