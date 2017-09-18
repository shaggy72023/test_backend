from django.contrib.auth.models import User

from bb_user.api.exceptions.user import UserDoesNotExistAPIError


class UserAPIMixin(object):

    user = None

    def dispatch(self, *args, **kwargs):

        try:
            self.user = User.objects.get(id=kwargs['post_id'])

        except User.DoesNotExist:
            raise UserDoesNotExistAPIError()

        return super(UserAPIMixin, self).dispatch(*args, **kwargs)
