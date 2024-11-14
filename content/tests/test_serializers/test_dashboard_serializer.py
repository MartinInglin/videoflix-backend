from rest_framework.test import APITestCase
from datetime import date

from content.serializers import DashboardVideoSerializer


class DashboardSerializerTests(APITestCase):

    def setUp(self):
        self.dashboard_data = {
            "created_at": date(2023, 1, 1),
            "category": "drama",
            "thumbnail": "thumbnail.img",
        }

    def test_contains_expected_fields(self):
        serializer = DashboardVideoSerializer(instance=self.dashboard_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(["created_at", "category", "thumbnail"]))
