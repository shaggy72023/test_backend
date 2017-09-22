from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from bb_comment.services.comment import create
from bb_post.api.exceptions import PostUnknownAPIError
from bb_post.models import Post
from bb_user.api.exceptions.user import UserDoesNotExistAPIError

import hashlib
import hmac
import datetime


class CommentCreationTestCase(TestCase):

    def setUp(self):

        # Create user and valid secure headers
        self.user = User.objects.create_user('another_test_user', 'test_mail@gmail.com', 'test123')
        self.post = Post(subject='Test subject', content='Test content')
        self.post.save()

        t = datetime.datetime.utcnow()
        access_token = self.user.get_session_auth_hash() + t.strftime('%Y%m%d')

        datestamp = t.strftime('%Y%m%dT%H%M%SZ')
        string_to_sign = datestamp + str(self.user.id)
        signature = hmac.new(access_token, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
        signature = signature.encode('base-64').strip()

        self.factory = RequestFactory(HTTP_DATE=datestamp, HTTP_AUTHORIZATION=signature)

    def test_comment_creation(self):
        parameters = {
            'user_id': self.user.id,
            'post': self.post.id,
            'content': 'Test Comment'
        }

        request = self.factory.post('api/comments')

        # Correct data
        self.assertTrue(create(request, parameters))

        # Incorrect post id
        wrong_post_parameters = parameters
        wrong_post_parameters['post'] = self.post.id + 1
        self.assertRaises(PostUnknownAPIError, create, request, wrong_post_parameters)

        # Incorrect user id
        wrong_user_parameters = parameters
        wrong_user_parameters['user_id'] = self.user.id + 1
        self.assertRaises(UserDoesNotExistAPIError, create, request, wrong_user_parameters)

# Incorrect headers checked in "test_user.py" module, so there is no need to check it here.
