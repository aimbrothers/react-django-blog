from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        post_author = instance.author
        request_user = self.context['request'].user

        if post_author and request_user and post_author == request_user.username:
            return super().update(instance, validated_data)
        else:
            msg = 'You cannot update post from other users.'

            raise serializers.ValidationError(msg, code='authorization')


class PostShortSerializer(serializers.ModelSerializer):
    shortDescription = serializers.CharField(source='short_description')
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'shortDescription')
