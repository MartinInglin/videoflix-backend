from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from authentication.functions import send_verification_email
from authentication.serializers import RegistrationSerializer, VerificationSeriazlizer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create()
            token, created = Token.objects.get_or_create(user=user)
            send_verification_email(request, user, token.key)
            
            return Response(
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

class VerificationView(APIView):
    pass
#     permission_classes = [TokenauthAuthentication]

#     def post(self, request):
#         serializer = VerificationSeriazlizer(self, data=request.data)
#         serializer.save()