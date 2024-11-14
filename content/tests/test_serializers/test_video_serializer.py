from rest_framework.test import APITestCase

from content.serializers import VideoSerializer


class VideoSerializerTests(APITestCase):

    def setUp(self):
        self.video_data = {
            "title": "Video title",
            "hls_file": "video_file.m3u8",
            "timestamp": 0,
        }

    def test_contains_expected_fields(self):
        serializer = VideoSerializer(instance=self.video_data)
        data = serializer.to_representation(self.video_data)
        self.assertEqual(set(data.keys()), set(["title", "hls_file", "timestamp"]))