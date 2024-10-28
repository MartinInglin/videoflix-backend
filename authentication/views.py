from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from authentication.functions import send_verification_email
from authentication.serializers import RegistrationSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create()
            send_verification_email(user)
            
            return Response(
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
