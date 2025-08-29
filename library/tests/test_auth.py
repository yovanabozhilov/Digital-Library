from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.main_url = reverse('main')
        self.welcome_url = reverse('welcome')
        User.objects.create_user(username='existinguser', email='exist@example.com', password='existpass')

    def test_register_with_missing_fields(self):
        response = self.client.post(self.register_url, {
            'username': '',
            'email': 'test@example.com',
            'password': 'pass1234',
            'password2': 'pass1234',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Моля, попълнете всички полета.')

        response = self.client.post(self.register_url, {
            'username': 'user1',
            'email': '',
            'password': 'pass1234',
            'password2': 'pass1234',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Моля, попълнете всички полета.')

        response = self.client.post(self.register_url, {
            'username': 'user1',
            'email': 'test@example.com',
            'password': '',
            'password2': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Моля, попълнете всички полета.')

    def test_register_valid_user(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password2': 'securepass123'
        }, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.main_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_with_existing_username(self):
        response = self.client.post(self.register_url, {
            'username': 'existinguser',
            'email': 'newemail@example.com',
            'password': 'newpass1234',
            'password2': 'newpass1234'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Потребителското име вече съществува!')

    def test_register_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'password1',
            'password2': 'password2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Паролите не съвпадат!')


    def test_login_valid_user(self):
        response = self.client.post(self.login_url, {
            'username': 'existinguser',
            'password': 'existpass'
        }, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.main_url)

    def test_login_invalid_user(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Невалидни данни за вход!')

    def test_login_missing_fields(self):
        response = self.client.post(self.login_url, {
            'username': '',
            'password': 'something'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Моля, попълнете всички полета.')

        response = self.client.post(self.login_url, {
            'username': 'existinguser',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Моля, попълнете всички полета.')

        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Моля, попълнете всички полета.')


    def test_logout_redirects_to_welcome(self):
        self.client.login(username='existinguser', password='existpass')
        response = self.client.get(self.logout_url, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.welcome_url)
