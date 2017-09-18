import datetime
import hashlib
import hmac


from django.contrib.auth.models import User
from django.db import IntegrityError
from bb_user.api.exceptions.user import UsernameExistsAPIError, WrongCredentialsAPIError, UserDoesNotExistAPIError, \
    WrongAuthorizeHeadersAPIError
from django.contrib.auth import authenticate


def create(username, email, password):

    try:
        user = User.objects.create_user(username, email, password)

    # Not unique username
    except IntegrityError as e:
        raise UsernameExistsAPIError(e.message)

    return user


def login(username, password):
    user = authenticate(username=username, password=password)

    # Wrong credentials
    if user is None:
        raise WrongCredentialsAPIError('Wrong username or password')

    return user


def get(request, user_id):
    datestamp = request.META.get('HTTP_DATE')
    signature = request.META.get('HTTP_AUTHORIZATION')
    converted_date = datetime.datetime.strptime(datestamp, '%Y%m%dT%H%M%SZ')
    now = datetime.datetime.now()
    delta = now - converted_date
    if delta > datetime.timedelta(minutes=5) or signature is None:
        raise WrongAuthorizeHeadersAPIError()

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist as e:
        raise UserDoesNotExistAPIError(e.message)

    access_token = user.get_session_auth_hash()

    string_to_sign = datestamp + str(user_id)
    generated_signature = hmac.new(access_token, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    generated_signature = generated_signature.encode('base-64').strip()
    if generated_signature == signature:
        return user
    else:
        raise WrongAuthorizeHeadersAPIError()

