from bb_comment.api.forms.comment import CommentForm
from bb_post.api.exceptions import PostUnknownAPIError
from bb_post.models import Post
from bb_user.api.exceptions.user import FormValidationFailsApiError

import bb_user.services.user


def create(request, parameters):

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
