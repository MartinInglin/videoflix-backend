from rest_framework import serializers
from authentication.models import CustomUser
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.contrib.auth import get_user_model

signer = TimestampSigner()
User = get_user_model()


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
    

class UserVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        try:
            email = signer.unsign(token, max_age=3600)
            user = User.objects.get(email=email)
            return user
        except (SignatureExpired, BadSignature, User.DoesNotExist):
            raise serializers.ValidationError("Invalid or expired token.")

    def save(self):
        user = self.validated_data.get("token")
        user.is_active = True
        user.save()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        try:
            email = signer.unsign(token, max_age=3600)
            user = User.objects.get(email=email)
            self.context['user'] = user
            return token
        except (SignatureExpired, BadSignature, User.DoesNotExist):
            raise serializers.ValidationError("Invalid or expired token.")
        
    def save(self, **kwargs):
        user = self.context.get("user")
        password = kwargs.get("password")
        if user and password:
            user.set_password(password)
            user.save()





