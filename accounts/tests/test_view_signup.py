from django.test import TestCase
from django.urls import resolve, reverse
from .. import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..forms import SignUpForm


class SingUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.view = resolve(url)
        self.response = self.client.get(url)

    def test_signup_url(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        self.assertEquals(self.view.func, views.signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSingUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@gmail.com',
            'password1': 'qwerty@123',
            'password2': 'qwerty@123'
        }
        self.response = self.client.post(url, data=data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertEquals(self.response.status_code, 302)
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_not_create_user(self):
        self.assertFalse(User.objects.exists())
