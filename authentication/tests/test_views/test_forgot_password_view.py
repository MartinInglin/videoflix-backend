from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

from authentication.models import CustomUser

class ForgotPasswordTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password123",
            is_active=False,
        )

    def test_forgot_password(self):
        url = reverse("forgot_password")
        data = {"email": self.user.email}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_user_with_email(self):
        url = reverse("forgot_password")
        data = {"email": "no_user@example.com"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # @patch(
    #     "authentication.functions.send_verification_email",
    #     side_effect=Exception("Email send error"),
    # )
    # def test_send_email_fails(self, mocked_mail):
    #     url = reverse("forgot_password")
    #     data = {"email": self.user.email}

    #     response = self.client.post(url, data, format="json")
    #     self.user.refresh_from_db()
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)