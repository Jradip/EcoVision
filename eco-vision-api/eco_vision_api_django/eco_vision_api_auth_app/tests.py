from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')  
        self.user_data = {
            "username": "user",
            "email": "user@testing.com",
            "password": "user1234"
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        logger.info("STATUS REGISTER: %s", response.status_code)
        logger.info("DATA REGISTER: %s", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        self.assertEqual(response.data['user']['username'], self.user_data['username'])
        self.assertEqual(response.data['user']['level'], 0)
        self.assertEqual(response.data['user']['exp'], 0)

    def test_login_user(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(self.login_url, {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }, format='json')

        logger.info("STATUS LOGIN: %s", response.status_code)
        logger.info("DATA LOGIN: %s", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        self.assertEqual(response.data['user']['username'], self.user_data['username'])

    def test_refresh_token(self):
        reg_response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)

        refresh_token = reg_response.data['refresh_token']
        logger.info("REFRESH TOKEN ASAL: %s", refresh_token)

        response = self.client.post(self.refresh_url, {
            "refresh": refresh_token
        }, format='json')

        logger.info("STATUS REFRESH: %s", response.status_code)
        logger.info("DATA REFRESH: %s", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertTrue(response.data['access'])  # token baru tidak boleh kosong
