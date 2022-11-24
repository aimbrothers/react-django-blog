from rest_framework import serializers

from .models import Post
from tags.models import Tag


class SlugRelatedGetOrCreateField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get_or_create(**{self.slug_field: data})[0]
        except (TypeError, ValueError):
            self.fail("invalid")


class PostSerializer(serializers.ModelSerializer):
    tags = SlugRelatedGetOrCreateField(
        many=True, slug_field='label', queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author',
                  'tags', 'created_at', 'updated_at')

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
    tags = SlugRelatedGetOrCreateField(
        many=True, slug_field='label', queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'shortDescription',
                  'tags', 'created_at', 'updated_at')
