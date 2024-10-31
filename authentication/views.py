from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from authentication.functions import send_verification_email, verify_user
from authentication.serializers import RegistrationSerializer, VerificationSeriazlizer


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

    def patch(self, request):
        user_id = request.data.get('userId')
        token = request.data.get('token')

        success = verify_user(user_id, token)

        if success:
            return Response({"message": "Email verified"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)
    
# class LoginView():
#     token, created = Token.objects.get_or_create(user=user)