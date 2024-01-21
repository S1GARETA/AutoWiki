from rest_framework import serializers
from .models import ForumPost, ForumComment

class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'comments_count',]

class ForumPostAllSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='auto.car_brand', read_only=True)
    model = serializers.CharField(source='auto.car_model', read_only=True)
    section = serializers.CharField(source='section.slug', read_only=True)

    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'comments_count', 'brand', 'model', 'section']

class ForumOnePostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'content', 'created_at', 'username']

class ForumCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ForumComment
        fields = ['id', 'content', 'created_at', 'username']