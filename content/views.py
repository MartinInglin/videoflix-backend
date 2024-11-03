from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from requests import Response
from rest_framework.views import APIView
from content.models import Video
from content.serializers import DashboardSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

class DashboardView(APIView):

    def get(self, request):
        data = Video.objects.all()
        serializer = DashboardSerializer(data, many=True)
        return Response(serializer.data)
