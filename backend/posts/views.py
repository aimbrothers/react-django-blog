from rest_framework import status, views, permissions
from rest_framework.response import Response

from backend.utils.authentications import SafeGetJWTAuthentication
from .models import Post
from .serializers import PostSerializer, PostShortSerializer


class PostView(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (SafeGetJWTAuthentication,)

    def get(self, request, pk=None):
        if pk:
            post = Post.objects.get(pk=pk)

            if post:
                data = PostSerializer(post)
        else:
            posts = Post.objects.all()

            if posts:
                data = PostShortSerializer(posts, many=True)

        if data:
            return Response(data.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PostSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, format=None, pk=None):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(
            instance=post, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, format=None, pk=None):
        post = Post.objects.get(pk=pk)

        current_user = request.user

        if post.author and current_user.username and post.author != current_user.username:
            msg = 'You cannot delete post from other users.'

            return Response({msg}, status=status.HTTP_400_BAD_REQUEST)

        if post:
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
