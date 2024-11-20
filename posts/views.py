from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Post, Tag, Comment, Notification, Vote
from .serializers import PostSerializer, CommentSerializer, NotificationSerializer, VoteSerializer
from django.db.models import Count
from datetime import datetime
from rest_framework import generics
from .serializers import TagSerializer


# List and Create Posts
class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all().annotate(like_count=Count('likes')).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Retrieve, Update, and Delete Posts
class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.view_count += 1
        post.save()
        return super().get(request, *args, **kwargs)

# Like a Post
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

        post.likes.add(request.user)
        total_likes = post.likes.count()
        return Response({'message': 'Post liked successfully', 'total_likes': total_likes}, status=200)

# Unlike a Post
class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

        post.likes.remove(request.user)
        total_likes = post.likes.count()
        return Response({'message': 'Post unliked successfully', 'total_likes': total_likes}, status=200)

# Comment on Post
class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Search Posts
class PostSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q', '')
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# Filter Posts by Tags
class FilterPostsByTagsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = request.GET.get('tags')
        posts = Post.objects.all()

        if tags:
            posts = posts.filter(tags__name__in=tags.split(','))

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# View Notifications
class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

# Upvote/Downvote Post
class VotePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        vote_type = request.data.get('vote_type')
        if vote_type not in ['up', 'down']:
            return Response({'error': 'Invalid vote type'}, status=400)

        post = Post.objects.get(id=post_id)
        Vote.objects.create(user=request.user, post=post, vote_type=vote_type)
        return Response({'message': f'Post {vote_type}voted successfully'}, status=200)

#create tags
class TagCreateView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
