from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from authentication.functions import (
    get_user_from_token,
    send_reset_password_email,
    send_verification_email,
)
from authentication.serializers import (
    RegistrationSerializer,
    ResetPasswordSerializer,
    UserVerificationSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create()
            send_verification_email(request, user)

            return Response(
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User successfully verified"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")
        user = get_user_from_token(identifier)

        if not user:
            try:
                user = User.objects.get(email=identifier)
            except:
                return Response(
                    {"message": "Something went wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        try:
            send_verification_email(request, user)
            return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class ForgotPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        try:
            send_reset_password_email(request, email)
            return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get("password")
            serializer.save(password=password)
            return Response(
                {"message": "Password successfully reset"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            Token.objects.filter(user=user).delete()

            token, created = Token.objects.get_or_create(user=user)

            data = {
                "email": user.email,
                "token": token.key,
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"message": "Successfully logged out"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "Something went wrong", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
