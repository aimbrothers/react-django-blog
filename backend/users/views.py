from rest_framework import permissions, views, status
from rest_framework.response import Response

from users.models import BackendUser

from . import serializers


class RegisterView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        backend_user: BackendUser = serializer.validated_data['user']
        backend_user_serializer = serializers.BackendUserSerializer(
            backend_user)

        return Response(backend_user_serializer.data, status=status.HTTP_201_CREATED)


class CurrentUserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = serializers.BackendUserSerializer(request.user)

        return Response(serializer.data)