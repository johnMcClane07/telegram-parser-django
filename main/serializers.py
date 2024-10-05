from rest_framework import serializers
from .models import Comment, Post

class CommentSerializer(serializers.ModelSerializer):
    post_link = serializers.CharField(source='post.link', read_only=True)
    post_company = serializers.CharField(source='post.company', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
