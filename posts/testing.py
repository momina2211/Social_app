from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Tag, Comment, Notification, Vote
from rest_framework.test import APIClient

class PostTests(TestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')

        # Create test tag
        self.tag = Tag.objects.create(name='testtag')

        # Create test post
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)

        # Create APIClient
        self.client = APIClient()

    def test_create_post(self):
        # Test POST request to create a new post
        self.client.login(username='testuser', password='password123')
        data = {'title': 'New Post', 'content': 'This is a new post.'}
        response = self.client.post(reverse('post_list_create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_post_detail(self):
        # Test GET request for a post's detail
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Post')

    def test_like_post(self):
        # Test liking a post
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('like_post', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, self.post.likes.all())

    def test_unlike_post(self):
        # Test unliking a post
        self.client.login(username='testuser', password='password123')
        self.post.likes.add(self.user)  # Initially like the post
        response = self.client.post(reverse('unlike_post', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user, self.post.likes.all())

    def test_comment_on_post(self):
        # Test adding a comment to a post
        self.client.login(username='testuser', password='password123')
        data = {'content': 'This is a comment.'}
        response = self.client.post(reverse('comment_list_create', kwargs={'post_id': self.post.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_post_search(self):
        # Test searching for a post
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('post_search'), {'q': 'Test Post'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_posts_by_tag(self):
        # Test filtering posts by tag
        self.client.login(username='testuser', password='password123')
        self.post.tags.add(self.tag)  # Assign the tag to the post
        response = self.client.get(reverse('filter_posts_by_tags'), {'tags': 'testtag'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_notification_creation(self):
        # Test creating notifications
        self.client.login(username='testuser', password='password123')
        Notification.objects.create(user=self.user, message='This is a test notification.')
        response = self.client.get(reverse('notification_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_vote_on_post(self):
        # Test voting (upvote/downvote) on a post
        self.client.login(username='testuser', password='password123')
        data = {'vote_type': 'up'}
        response = self.client.post(reverse('vote_post', kwargs={'post_id': self.post.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().vote_type, 'up')

    def test_post_view_count(self):
        # Test if post view count increases
        initial_view_count = self.post.view_count
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, initial_view_count + 1)


class TagTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_create_tag(self):
        # Test creating a tag
        self.client.login(username='testuser', password='password123')
        data = {'name': 'newtag'}
        response = self.client.post(reverse('tag_list_create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)


class VoteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)

    def test_vote_up(self):
        # Test upvote
        self.client.login(username='testuser', password='password123')
        data = {'vote_type': 'up'}
        response = self.client.post(reverse('vote_post', kwargs={'post_id': self.post.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vote.objects.filter(vote_type='up').count(), 1)

    def test_vote_down(self):
        # Test downvote
        self.client.login(username='testuser2', password='password123')
        data = {'vote_type': 'down'}
        response = self.client.post(reverse('vote_post', kwargs={'post_id': self.post.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vote.objects.filter(vote_type='down').count(), 1)
