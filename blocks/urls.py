from django.urls import path
from .views import BlockUserView, UnblockUserView, BlockedUsersListView

urlpatterns = [
    path('<int:user_id>/block/', BlockUserView.as_view(), name='block_user'),
    path('<int:user_id>/unblock/', UnblockUserView.as_view(), name='unblock_user'),
    path('blocked-users/', BlockedUsersListView.as_view(), name='blocked_users_list'),
]
