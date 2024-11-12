from rest_framework.test import APITestCase
from rest_framework import serializers
from authentication.models import CustomUser
from authentication.serializers import RegistrationSerializer


class RegistrationSerializerTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser@example.com",
            "email": "testuser@example.com",
            "password": "password123",
        }

    def test_contains_expected_fields(self):
        serializer = RegistrationSerializer(instance=self.user_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['email']))

    def test_create(self):
        serializer = RegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        created_user = serializer.create()

        self.assertEqual(created_user.username, self.user_data["username"])
        self.assertEqual(created_user.email, self.user_data["email"])
        self.assertTrue(created_user.check_password(self.user_data["password"]))
        self.assertFalse(created_user.is_active)

    def test_password_is_hashed(self):
        serializer = RegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        created_user = serializer.create()

        self.assertNotEqual(created_user.password, self.user_data["password"])
        self.assertTrue(created_user.check_password(self.user_data["password"]))

    def test_missing_required_fields(self):
        incomplete_data = {
            "email": "testuser@example.com",
        }
        serializer = RegistrationSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_validate_email(self):
        email_user2 = "existing@email.com"
        serializer = RegistrationSerializer()
        response = serializer.validate_email(self.user_data["username"])
        self.assertNotEqual(response, email_user2)

    def test_email_already_exists(self):
        CustomUser.objects.create_user(**self.user_data)
        serializer = RegistrationSerializer()

        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.validate_email(self.user_data["username"])

        self.assertEqual(str(cm.exception.detail[0]), "error")
