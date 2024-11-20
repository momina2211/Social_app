from django.urls import path
from .views import FollowUserView, UnfollowUserView, FollowersListView, FollowingListView

urlpatterns = [
    path('<int:user_id>/follow/', FollowUserView.as_view(), name='follow_user'),
    path('<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='user_followers'),
    path('<int:user_id>/following/', FollowingListView.as_view(), name='user_following'),
]
