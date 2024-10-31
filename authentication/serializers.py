from rest_framework import serializers
from authentication.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def create(self):
        username = self.validated_data["email"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]

        if self.emailExists(username):
            raise serializers.ValidationError("error")

        else:
            account = CustomUser(
                username=username, password=password, email=email, is_active=False
            )
            account.set_password(password)
            account.save()
            return account

    def emailExists(self, username):
        return CustomUser.objects.filter(username=username).exists()


class VerificationSeriazlizer(serializers.ModelSerializer):

    class Meta:
        model: CustomUser

    def update(self, instance, validated_data):
        validated_data.is_acitvated = True

        return super().update(instance, validated_data)
