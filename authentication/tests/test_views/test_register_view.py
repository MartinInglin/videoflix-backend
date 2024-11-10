from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest import mock


class RegistrationTests(APITestCase):

    def test_register_user(self):
        url = reverse("registration")
        data = {
            "password": "password123",
            "email": "testuser@example.com",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_no_email(self):
        url = reverse("registration")
        data = {
            "password": "password123",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_register_no_password(self):
        url = reverse("registration")
        data = {
            "email": "testuser@example.com",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_email(self):
        url = reverse("registration")
        data = {"password": "password123", "email": "this_is_no_email"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_sending_failure(self):
        with mock.patch("authentication.functions.send_verification_email") as mocked_mail:
            mocked_mail.side_effect = Exception("Email send error")

        url = reverse("registration")
        data = {
            "password": "password123",
            "email": "testuser@example.com",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
