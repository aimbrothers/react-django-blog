from django.contrib.auth import login, logout

from rest_framework import permissions, views, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from users.models import BackendUser

from . import serializers


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(
            data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):
    def post(self, request, format=None):
        logout(request)

        return Response(None, status=status.HTTP_202_ACCEPTED)


class RegisterView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        backend_user: BackendUser = serializer.validated_data['user']
        backend_user_serializer = serializers.BackendUserSerializer(
            backend_user)

        return Response(backend_user_serializer.data, status=status.HTTP_201_CREATED)
