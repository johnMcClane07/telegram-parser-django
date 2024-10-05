from rest_framework import serializers
from main.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'company', 'link'] 

class PostRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения деталей поста.

    Возвращает подробную информацию о посте, включая количество комментариев,
    количество позитивных, негативных и нейтральных комментариев, а также
    количество номеров телефонов.
    """
    comments = CommentSerializer(many=True)
    length = serializers.IntegerField(read_only=True)
    positive = serializers.IntegerField(read_only=True)
    negative = serializers.IntegerField(read_only=True)
    neutral = serializers.IntegerField(read_only=True)
    phones=serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'company', 'link', 'length', 'comments', 'positive', 'negative', 'neutral', 'phones']
