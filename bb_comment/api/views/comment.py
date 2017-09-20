from django.views.generic import View

from bb_comment.api.forms.comment import CommentForm
from bb_post.api.exceptions import PostUnknownAPIError
from bb_post.models import Post
from bb_user.api.exceptions.user import FormValidationFailsApiError
from utils.api.mixins import APIMixin

import bb_user.services.user
import json


class Comment(APIMixin, View):

    def post(self, request, parameters):
        parameters = json.loads(parameters)

        # Validate secure headers and check if user and post exists
        user = bb_user.services.user.get(request, parameters['user_id'])
        post_exists = Post.objects.filter(id=parameters['post']).exists()

        if not post_exists:
            raise PostUnknownAPIError()

        parameters['author'] = user.id
        form = CommentForm(parameters)
        if not form.is_valid():
            raise FormValidationFailsApiError(form.errors)

        form.save()
        return True

