from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
            first_name='Test',
            last_name='User1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            password='testpass123',
            first_name='Test',
            last_name='User2'
        )

    def test_user_list_view(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertContains(response, 'testuser1')
        self.assertContains(response, 'testuser2')

    def test_user_create_view(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('create'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User', 
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        
        self.assertRedirects(response, reverse('login'))
        
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_own_profile(self):
        self.client.login(username='testuser1', password='testpass123')
        
        response = self.client.post(reverse('update', kwargs={'user_id': self.user1.id}), {
            'first_name': 'Updated',
            'last_name': 'Name'
        })
        
        self.assertRedirects(response, reverse('user_list'))
        
        updated_user = User.objects.get(id=self.user1.id)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')

    def test_user_cannot_update_other_profile(self):
        self.client.login(username='testuser1', password='testpass123')
        
        response = self.client.get(reverse('update', kwargs={'user_id': self.user2.id}))
        self.assertRedirects(response, reverse('user_list'))

    def test_user_delete_own_profile(self):
        self.client.login(username='testuser1', password='testpass123')
        
        response = self.client.post(reverse('delete', kwargs={'user_id': self.user1.id}))
        self.assertRedirects(response, reverse('user_list'))
        
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_user_cannot_delete_other_profile(self):
        self.client.login(username='testuser1', password='testpass123')
        
        response = self.client.post(reverse('delete', kwargs={'user_id': self.user2.id}))
        self.assertRedirects(response, reverse('user_list'))
        
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_view(self):
        """Тест входа в систему"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertRedirects(response, reverse('index'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
