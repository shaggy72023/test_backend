# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from bb_user.api.exceptions.user import FormValidationFailsApiError, WrongActivationCodeApiError, UserDoesNotExistAPIError, \
    WrongAuthorizeHeadersAPIError, WrongCredentialsAPIError
from bb_user.services.user import create, activate, get, login

import hashlib
import hmac
import datetime


class UserCreationTestCase(TestCase):
    def test_user_creation(self):
        activation_url = 'http://localhost:8000/activate'

        parameters = {
            'email': 'test_mail@gmail.com',
            'username': 'test_user',
            'password1': 'test123',
            'password2': 'test123'
        }
        user = create(activation_url, parameters)
        self.user = user
        self.assertEqual(user.email, parameters['email'])
        self.assertEqual(user.username, parameters['username'])
        self.assertTrue(user.check_password(parameters['password1']))

        # Duplicate entry test case
        self.assertRaises(FormValidationFailsApiError, create, activation_url, parameters)

        # Password 1 didn't match password 2 case
        parameters['password1'] = 'test12'
        parameters['username'] = 'new_test_user'
        self.assertRaises(FormValidationFailsApiError, create, activation_url, parameters)

        # Confirmation code only valid for this values
        date = '20170921'
        confirmation_code = 'TQ5l3uK9slUXXcICzNoaE4Fte3sfTstySMiAYpKRnpk='

        # Wrong user id
        self.assertRaises(UserDoesNotExistAPIError, activate, self.user.id + 1, confirmation_code, activation_url, date)

        # Wrong confirmation code
        self.assertRaises(WrongActivationCodeApiError, activate, self.user.id, confirmation_code + "1", activation_url, date)

        # Correct confirmation code
        self.assertTrue(activate(self.user.id, confirmation_code, activation_url, date=date))


class UserGettingTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('another_test_user', 'test_mail@gmail.com', 'test123')
        t = datetime.datetime.utcnow()
        access_token = self.user.get_session_auth_hash() + t.strftime('%Y%m%d')

        datestamp = t.strftime('%Y%m%dT%H%M%SZ')
        string_to_sign = datestamp + str(self.user.id)
        signature = hmac.new(access_token, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
        signature = signature.encode('base-64').strip()

        self.factory = RequestFactory(HTTP_DATE=datestamp, HTTP_AUTHORIZATION=signature)

        # 10 minutes between request and server time case
        t -= datetime.timedelta(minutes=10)
        datestamp = t.strftime('%Y%m%dT%H%M%SZ')

        self.wrong_date_factory = RequestFactory(HTTP_DATE=datestamp, HTTP_AUTHORIZATION=signature)

        self.wrong_signature_factory = RequestFactory(HTTP_DATE=datestamp, HTTP_AUTHORIZATION=signature + "abc")

    def test_getting_user(self):
        request = self.factory.get('/api/users/{}'.format(self.user.id))
        user = get(request, self.user.id)

        # Correct data
        self.assertEqual(user.id, self.user.id)

        # Wrong user id
        self.assertRaises(UserDoesNotExistAPIError, get, request, self.user.id + 1)

        # 10 minutes between request and server time
        wrong_time_request = self.wrong_date_factory.get('/api/users/{}'.format(self.user.id))
        self.assertRaises(WrongAuthorizeHeadersAPIError, get, wrong_time_request, self.user.id)

        # Wrong signature request
        wrong_signature_request = self.wrong_signature_factory.get('/api/users/{}'.format(self.user.id))
        self.assertRaises(WrongAuthorizeHeadersAPIError, get, wrong_signature_request, self.user.id)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('one_more_test_user', 'test_mail@gmail.com', 'test123')

    def test_login_user(self):
        user = login('one_more_test_user', 'test123')

        # Correct login
        self.assertEqual(user.id, self.user.id)

        # Wrong password
        self.assertRaises(WrongCredentialsAPIError, login, 'one_more_test_user', 'test')

        # Wrong username
        self.assertRaises(WrongCredentialsAPIError, login, 'one_test_user', 'test123')