from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from authentication.models import CustomUser

class LogoutTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.get_or_create(
            username="testuser", password="test1234"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)