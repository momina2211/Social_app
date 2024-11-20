from django.db import models
from django.contrib.auth.models import User

class BlockedUser(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')  # Prevent duplicate blocks.

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"
