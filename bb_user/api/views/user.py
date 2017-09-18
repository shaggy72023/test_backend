import json

from django.views.generic import View

from bb_user.api.forms.user import SignUpForm, LoginForm
from utils.api.exceptions import RequestValidationFailedAPIError
from utils.api.mixins import APIMixin
from bb_user.api.serializers.user import serialize, serialize_access_token

import bb_user.services.user


class User(APIMixin, View):

    def post(self, request, parameters):
        parameters = json.loads(parameters)
        form = SignUpForm(data=parameters)

        if form.is_valid():
            user = bb_user.services.user.create(**form.cleaned_data)
            return serialize_access_token(user)

        else:
            raise RequestValidationFailedAPIError(form.errors)

    def get(self, request, user_id, parameters):
        user = bb_user.services.user.get(request, user_id)
        return serialize(user)


class LoginUser(User):

    def post(self, request, parameters):
        parameters = json.loads(parameters)
        form = LoginForm(data=parameters)

        if form.is_valid():
            user = bb_user.services.user.login(**form.cleaned_data)
            return serialize_access_token(user)

        else:
            raise RequestValidationFailedAPIError(form.errors)

