from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from unittest.mock import patch

from user.models import User
from user.tokens import TokenGenerator
from app.tests import BaseAPITest


class TestObtainJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "hijack@mail.com"
        self.password = "hi"
        self.user = self.create(email=self.email, password=self.password)

    def test_auth(self):
        data = {'email': self.email, 'password': self.password}
        resp = self.client.post(reverse('v1:user:obtain'), data=data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_auth_wrong_pass(self):
        data = {'email': self.email, 'password': 'wrong_pass'}
        resp = self.client.post(reverse('v1:user:obtain'), data=data)
        self.assertEqual(resp.status_code, 401)

    def test_auth_wrong_email(self):
        data = {'email': 'wrong_email', 'password': self.password}
        resp = self.client.post(reverse('v1:user:obtain'), data=data)
        self.assertEqual(resp.status_code, 401)


class TestVerifyJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "hijack@mail.com"
        self.password = "hi"
        self.user = self.create(email=self.email, password=self.password)
        self.access_token = str(AccessToken.for_user(self.user))

    def test_token_is_valid(self):
        data = {'token': self.access_token}
        resp = self.client.post(reverse('v1:user:verify'), data=data)
        self.assertEqual(resp.status_code, 200)

    def test_get_token_validation_error(self):
        data = {'token': 'fake_data'}
        resp = self.client.post(reverse('v1:user:verify'), data=data)
        self.assertEqual(resp.status_code, 401)


class TestRefreshJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "hijack@mail.com"
        self.password = "hi"
        self.user = self.create(email=self.email, password=self.password)
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def test_get_access_token(self):
        data = {'refresh': self.refresh_token}
        resp = self.client.post(reverse('v1:user:refresh'), data=data)
        self.assertIn('access', resp.data)

    def test_get_token_refresh_error(self):
        data = {'refresh': 'fake_data'}
        resp = self.client.post(reverse('v1:user:refresh'), data=data)
        self.assertEqual(resp.status_code, 401)


class TestSignUpView(BaseAPITest):

    def setUp(self):
        self.data = {
            "email": "hijack@test.com",
            "password": "hi",
            "path": "/activate/",
        }

    @patch('user.tasks.send_email.delay')
    def test_sign_up(self, email_delay):
        resp = self.client.post(reverse('v1:user:sign-up'), data=self.data)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(User.objects.filter(email=self.data['email']).exists())
        email_delay.assert_called_once()

    @patch('user.tasks.send_email.delay')
    def test_sign_up_email_to_lower_case(self, email_delay):
        self.data['email'] = 'hiJACK@mail.com'
        resp = self.client.post(reverse('v1:user:sign-up'), data=self.data)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(User.objects.filter(email=self.data['email'].lower(),).exists())
        email_delay.assert_called_once()

    def test_sign_up_user_exists(self):
        email = 'test@test.com'
        self.create(email=email)
        self.data['email'] = email
        resp = self.client.post(reverse('v1:user:sign-up'), data=self.data)
        self.assertEqual(resp.status_code, 400)


class TestActivateUserView(BaseAPITest):

    def setUp(self):
        self.email = "hijack@mail.com"
        self.password = "hi"
        self.user = self.create(email=self.email, password=self.password)
        self.user.is_active = False
        self.user.save()

    def test_user_activation(self):
        token = f"{urlsafe_base64_encode(force_bytes(self.user.email))}.{TokenGenerator.make_token(self.user)}"
        data = {'token': token}
        resp = self.client.post(reverse('v1:user:activate'), data=data)
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(user.is_active)
        self.assertTrue('access_token' in resp.data.keys())
        self.assertTrue('refresh_token' in resp.data.keys())

    def test_user_activation_wrong_uid(self):
        token = f"hijack.{TokenGenerator.make_token(self.user)}"
        data = {'token': token}
        resp = self.client.post(reverse('v1:user:activate'), data=data)
        self.assertEqual(resp.status_code, 400)

    def test_user_activation_wrong_token(self):
        token = f"{urlsafe_base64_encode(force_bytes(self.user.email))}.hijack"
        data = {'token': token}
        resp = self.client.post(reverse('v1:user:activate'), data=data)
        self.assertEqual(resp.status_code, 400)

    def test_user_activation_user_does_not_exists(self):
        token = f"{urlsafe_base64_encode(force_bytes('wrong@email.com'))}.{TokenGenerator.make_token(self.user)}"
        data = {'token': token}
        resp = self.client.post(reverse('v1:user:activate'), data=data)
        self.assertEqual(resp.status_code, 400)
