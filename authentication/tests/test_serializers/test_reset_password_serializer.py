from rest_framework import serializers
from rest_framework.test import APITestCase
from django.core.signing import (
    TimestampSigner,
)
from authentication.models import CustomUser
from authentication.serializers import (
    ResetPasswordSerializer,
)
from freezegun import freeze_time


class ResetPasswordTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password123",
            is_active=False,
        )
        self.signer = TimestampSigner()
        self.valid_token = self.signer.sign(self.user.email)

    def test_valid_token(self):
        serializer = ResetPasswordSerializer(data={"token": self.valid_token})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["token"], self.valid_token)

    @freeze_time("2023-01-01 12:00:00")
    def test_expired_token(self):
        token = self.signer.sign(self.user.email)
        with self.assertRaises(serializers.ValidationError):
            serializer = ResetPasswordSerializer(data={"token": token})
            with freeze_time("2023-01-02 14:00:00"):
                serializer.is_valid(raise_exception=True)

    def test_bad_signature(self):
        serializer = ResetPasswordSerializer(data={"token": "invalidtoken"})
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_non_existent_user(self):
        fake_token = self.signer.sign("nonexistent@example.com")
        serializer = ResetPasswordSerializer(data={"token": fake_token})
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_save_password(self):
        new_password = "new_password"
        serializer = ResetPasswordSerializer(data={"token": self.valid_token})
        self.assertTrue(serializer.is_valid(), serializer.errors)

        serializer.save(password=new_password)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
