from rest_framework import status, views, permissions, filters
from rest_framework.response import Response
from django_filters import rest_framework as django_filters

from backend.utils.authentications import SafeGetJWTAuthentication
from .models import Post
from .serializers import PostSerializer, PostShortSerializer


class PostFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__label')
    
    class Meta:
        model = Post
        fields = ('tags',)


class PostView(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (SafeGetJWTAuthentication,)
    filter_backends = (filters.SearchFilter, django_filters.DjangoFilterBackend,)
    search_fields = ['title', 'content', 'user__username', 'tags__label']
    filterset_class = PostFilter

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        
        return queryset

    def get(self, request, pk=None):
        if pk:
            post = Post.objects.get(pk=pk)

            if post:
                serializer = PostSerializer(post)
        else:
            posts_queryset = Post.objects.all()
            filtered_posts_queryset = self.filter_queryset(posts_queryset)

            if posts_queryset:
                serializer = PostShortSerializer(filtered_posts_queryset, many=True)

        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
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
