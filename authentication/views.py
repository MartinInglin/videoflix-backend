from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from authentication.functions import get_user_from_token, send_reset_password_email, send_verification_email
from authentication.serializers import RegistrationSerializer, ResetPasswordSerializer, UserVerificationSerializer

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
            return Response({"message": "User successfully verified"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ResendVerificationEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        user = get_user_from_token(token)

        try:
            send_verification_email(request, user)
            return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
class ForgotPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            send_reset_password_email(request, email)
            return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get("password")
            serializer.save(password=password)
            return Response({"message": "Password successfully reset"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
# class LoginView():
#     token, created = Token.objects.get_or_create(user=user)