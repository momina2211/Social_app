# users/views.py
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from follows.models import Follow
from blocks.models import BlockedUser
from posts.models import Post
from .serializer import UserRegisterSerializer, UserSerializer, ProfileSerializer, FollowSerializer, BlockedUserSerializer

# Register a new user
class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

# View or update profile details
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# Follow a user
class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = {'follower': request.user.id, 'following': request.data.get('following')}
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Block a user
class BlockUserView(generics.CreateAPIView):
    serializer_class = BlockedUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = {'blocker': request.user.id, 'blocked': request.data.get('blocked')}
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Like/Unlike a post
class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            message = 'Post unliked'
        else:
            post.likes.add(request.user)
            message = 'Post liked'

        return Response({'message': message, 'post_id': post.id})
