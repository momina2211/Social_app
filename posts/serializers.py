from rest_framework import serializers
from .models import Post, Comment, Tag, Notification, Vote

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',  # Use 'name' field of the Tag model for serialization and deserialization
        queryset=Tag.objects.all()  # Ensure tags can be looked up by their name
    )
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    view_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'tags', 'created_at', 'updated_at', 'likes', 'comment_count', 'like_count', 'view_count']
        read_only_fields = ['created_at', 'updated_at', 'likes', 'comment_count', 'like_count', 'view_count']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']
        read_only_fields = ['created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at']
        read_only_fields = ['created_at']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user', 'post', 'vote_type', 'created_at']
        read_only_fields = ['created_at']
