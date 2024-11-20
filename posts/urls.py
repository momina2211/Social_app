from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    LikePostView,
    UnlikePostView,
    CommentListCreateView,
    PostSearchView,
    FilterPostsByTagsView,
    NotificationListView,
    VotePostView,
    TagCreateView
)

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post_list_create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike_post'),
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment_list_create'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('filter/', FilterPostsByTagsView.as_view(), name='filter_posts_by_tags'),
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('<int:post_id>/vote/', VotePostView.as_view(), name='vote_post'),
path('tags/create/', TagCreateView.as_view(), name='create_tag'),

]
