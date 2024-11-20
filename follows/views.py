from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Follow
from .serializers import FollowSerializer

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if follower == following:
            return Response({'error': 'You cannot follow yourself'}, status=400)

        follow, created = Follow.objects.get_or_create(follower=follower, following=following)
        if not created:
            return Response({'message': 'Already following'}, status=200)

        return Response({'message': 'Followed successfully'}, status=201)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        try:
            follow = Follow.objects.get(follower=follower, following=following)
            follow.delete()
        except Follow.DoesNotExist:
            return Response({'error': 'You are not following this user'}, status=400)

        return Response({'message': 'Unfollowed successfully'}, status=200)


class FollowersListView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        followers = user.followers.all()
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)


class FollowingListView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        following = user.following.all()
        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data)
