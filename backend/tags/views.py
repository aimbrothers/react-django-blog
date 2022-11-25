from rest_framework import generics, permissions

from .serializers import TagSerializer
from .models import Tag


class TagView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer