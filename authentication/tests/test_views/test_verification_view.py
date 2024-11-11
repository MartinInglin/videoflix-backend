from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.signing import TimestampSigner
from freezegun import freeze_time
from authentication.models import CustomUser
from unittest.mock import patch

from authentication.serializers import UserVerificationSerializer


class VerificationTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password123",
            is_active=False,
        )
        self.signer = TimestampSigner()

    def test_verficate_user(self):
        url = reverse("verification")
        token = self.signer.sign(self.user.email)
        data = {"token": token}

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_active)

    def test_no_token(self):
        url = reverse("verification")
        data = {}

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_token(self):
        url = reverse("verification")
        data = {"token": "testuser@example.com123456"}

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2023-01-01 12:00:00")
    def test_expired_token(self):
        token = self.signer.sign(self.user.email)

        with freeze_time("2023-01-01 14:01:00"):
            url = reverse("verification")
            data = {"token": token}

            response = self.client.post(url, data, format="json")
            self.user.refresh_from_db()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(
        UserVerificationSerializer, "save", side_effect=Exception("Save failed")
    )
    def test_save_failed(self, mock_save):
        url = reverse("verification")
        token = self.signer.sign(self.user.email)
        data = {"token": token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
