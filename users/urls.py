# users/urls.py
from django.urls import path
from .views import RegisterUserView, ProfileView, FollowUserView, BlockUserView, LikePostView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/', FollowUserView.as_view(), name='follow-user'),
    path('block/', BlockUserView.as_view(), name='block-user'),
    path('like-post/', LikePostView.as_view(), name='like-post'),
]
