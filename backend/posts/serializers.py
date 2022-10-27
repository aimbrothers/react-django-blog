from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'author')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)