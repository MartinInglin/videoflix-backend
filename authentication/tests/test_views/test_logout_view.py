from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from authentication.models import CustomUser
from unittest.mock import patch

class LogoutTests(APITestCase):
    def setUp(self):
        self.user, created = CustomUser.objects.get_or_create(
            username="testuser", password="test1234"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_logout(self):
        url = reverse("logout")
        
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_token(self):
        self.client.credentials()

        url = reverse("logout")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        self.token = '123456'
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        url = reverse("logout")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch(
        "rest_framework.authtoken.models.Token.delete",
        side_effect=Exception("Token deletion failed"),
    )
    def test_delete_token_fails(self, mock_delete):
        url = reverse("logout")
        
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)