from django.test import TestCase, RequestFactory, LiveServerTestCase, Client
from selenium import webdriver
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.sessions.middleware import SessionMiddleware
from .views import signup
from .models import AllLogins


class AdminViewTest(TestCase):
    def test_admin_permisiion(self):
        admin_user = User.objects.create(email='admin@gmail.com',password='admin997',is_staff=True)
        factory = RequestFactory()
        request = factory.get('/')
        request.user = admin_user
        permission = permissions.IsAdminUser()
        has_permission = permission.has_permission(request, None)
        self.assertTrue(has_permission)

class RegistrationViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
    
    def test_post_request_creates_new_user(self):
        data = {
            'first_name': 'newuser',
            'last_name': 'olduser',
            'username': 'newold',
            'email': 'new_user@email.com',
            'screen_name': 'new_user',
            'password': 'new_user_password',
            'password_confirm': 'new_user_password',
        }
        request = self.factory.post('signup/', data )
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        response = signup(request)
        
        with self.assertTemplateUsed('signup.html'):
            self.assertEqual(response.status_code, 200)

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_model_alllogins(self):
        all_logins = AllLogins.objects.create(
            user = self.user,
            ip_address = '127.0.0.1',
            server = 'server01'
        )
    self.assertTrue(isinstance(all_logins, AllLogins))

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # urls
        self.index_url = reverse('index')
        self.dashboard_url = reverse('dashboard')
        self.login_url = reverse('login')

    def test_index_GET(self):
        # mock the response
        response = self.client.get(self.index_url)

        # write assertions
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_dashboard_GET(self):
        # mock the response
        response = self.client.get(self.dashboard_url)

        # write assertions
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_GET_not_logged_in(self):
        self.client.logout()

        response = self.client.get(self.dashboard_url)

        # write assertions
        self.assertEquals(response.status_code, 302)

    def test_add_logins_POST(self):
        response = self.client.post(self.login_url, {
            "user": self.user.id,
            "username": self.user.username,
            "ip_address": '127.0.0.1',
            "server": 'server01'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(AllLogins.objects.count(), 2)
        self.assertEquals(AllLogins.objects.last().server, 'server01')

    def test_logins_POST_no_data(self):
        response = self.client.post(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(AllLogins.objects.count(), 1)

        
class LoginTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='password')

	def test_login_with_valid_credentials(self):
		response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
		self.assertRedirects(response, reverse('dashboard')) #Assuming 'dashboard' is the URL to redirect after login

	def test_login_with_invalid_credentials(self):
		response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
		self.assertEqual(response.status_code, 200) #Assuming login page is rendered again with error message
		self.assertContains(response, 'Invalid username or password')

	def test_login_with_inactive_user(self):
		self.user.is_active = False
		self.user.save()
		response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Account is inactive')


class SignupTestCase(TestCase):
    def test_can_add_new_user(self):
        raise NotImplementedError()