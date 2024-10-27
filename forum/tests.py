from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Thread, Post, Food
from .forms import ThreadForm, PostForm

User = get_user_model()

class ForumTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', email='user@test.com', password='12345')
        self.client.login(username='testuser', password='12345')

        # Create a sample food item with required fields
        self.food = Food.objects.create(name='Sample Food', price=10.00)

        # Create a thread for testing
        self.thread = Thread.objects.create(title='Test Thread', user=self.user)
        self.thread.foods.add(self.food)

        # Create a post for testing
        self.post = Post.objects.create(content='Test Post Content', thread=self.thread, user=self.user)

    def test_thread_list_view(self):
        response = self.client.get(reverse('forum:thread_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Thread')

    def test_thread_detail_view(self):
        url = reverse('forum:thread_detail', args=[self.thread.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post Content')

    def test_create_thread(self):
        response = self.client.post(reverse('forum:create_thread_ajax'), {
            'title': 'New Thread',
            'food': self.food.name
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Thread.objects.count(), 2)

    def test_ajax_create_post(self):
        response = self.client.post(reverse('forum:create_post_ajax', args=[self.thread.id]), {
            'content': 'Another Post'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 2)

    def test_edit_thread(self):
        url = reverse('forum:edit_thread', kwargs={'thread_id': self.thread.id})
        response = self.client.post(url, {'title': 'Updated Title'})
        self.assertEqual(response.status_code, 302)
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, 'Updated Title')

    def test_delete_thread(self):
        url = reverse('forum:delete_thread', kwargs={'thread_id': self.thread.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Thread.objects.count(), 0)

    # New tests for editing and deleting posts
    def test_edit_post(self):
        url = reverse('forum:edit_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url, {'content': 'Updated Post Content'})
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Updated Post Content')

    def test_delete_post(self):
        url = reverse('forum:delete_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

    def test_unauthorized_post_edit(self):
        # Create another user
        other_user = User.objects.create_user(username='otheruser', email='other@test.com', password='12345')
        self.client.logout()
        self.client.login(username='otheruser', password='12345')

        url = reverse('forum:edit_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url, {'content': 'Malicious Edit'})
        self.assertEqual(response.status_code, 404)  # Should return 404 since the user is not authorized

    def test_unauthorized_post_delete(self):
        # Create another user
        other_user = User.objects.create_user(username='otheruser', email='other@test.com', password='12345')
        self.client.logout()
        self.client.login(username='otheruser', password='12345')

        url = reverse('forum:delete_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)  # Should return 404 since the user is not authorized

    def test_search_threads(self):
        response = self.client.get(reverse('forum:thread_list'), {'q': 'Test Thread'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Thread')
        self.assertNotContains(response, 'Nonexistent Thread')