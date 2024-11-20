from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import BlockedUser
from .serializers import BlockedUserSerializer

class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        blocker = request.user
        try:
            blocked = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if blocker == blocked:
            return Response({'error': 'You cannot block yourself'}, status=400)

        block, created = BlockedUser.objects.get_or_create(blocker=blocker, blocked=blocked)
        if not created:
            return Response({'message': 'User is already blocked'}, status=200)

        return Response({'message': 'User blocked successfully'}, status=201)


class UnblockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        blocker = request.user
        try:
            blocked = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        try:
            block = BlockedUser.objects.get(blocker=blocker, blocked=blocked)
            block.delete()
        except BlockedUser.DoesNotExist:
            return Response({'error': 'User is not blocked'}, status=400)

        return Response({'message': 'User unblocked successfully'}, status=200)


class BlockedUsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blocked_users = BlockedUser.objects.filter(blocker=request.user)
        serializer = BlockedUserSerializer(blocked_users, many=True)
        return Response(serializer.data)
