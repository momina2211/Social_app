from rest_framework import serializers
from .models import BlockedUser

class BlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedUser
        fields = ['id', 'blocker', 'blocked', 'created_at']
