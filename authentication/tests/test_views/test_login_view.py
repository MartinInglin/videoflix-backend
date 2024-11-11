from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from authentication.models import CustomUser
from unittest.mock import patch


class LoginTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password123",
        )
        self.client = APIClient()

    def test_login(self):
        url = reverse("login")
        data = {
            "username": self.user.email,
            "password": "password123",
        }

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_authenticated)
        self.assertEqual(response.data.get("email"), self.user.email)
        self.assertTrue(response.data["token"])

    def test_wrong_password(self):
        url = reverse("login")
        data = {
            "username": self.user.email,
            "password": "wrong_password",
        }

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_existing(self):
        url = reverse("login")
        data = {
            "username": "not_existing@no_mail.com",
            "password": "password123",
        }

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_password(self):
        url = reverse("login")
        data = {
            "username": self.user.email,
        }

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_email(self):
        url = reverse("login")
        data = {
            "password": "password123",
        }

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        "rest_framework.authtoken.models.Token.objects.get_or_create",
        side_effect=Exception("Token creation failed"),
    )
    def test_token_creation_fails(self, mock_create):
        url = reverse("login")
        data = {
            "username": self.user.email,
            "password": "password123",
        }

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
