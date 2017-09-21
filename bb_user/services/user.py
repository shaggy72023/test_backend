import datetime
import hashlib
import hmac

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail

from bb_user.api.exceptions.user import FormValidationFailsApiError, WrongCredentialsAPIError, UserDoesNotExistAPIError, \
    WrongAuthorizeHeadersAPIError, WrongActivationCodeApiError
from bb_user.api.forms.user import SignUpForm
from blog_backend import settings


def create(activation_url, parameters):
    form = SignUpForm(data=parameters)

    if not form.is_valid():
        errors_list = []
        for error_key in form.errors:
            errors_list.append(form.errors[error_key][0])
        raise FormValidationFailsApiError(errors_list)

    user = form.save(commit=False)
    user.is_active = False
    user.save()

    key = activation_url + settings.SECRET_KEY + datetime.datetime.utcnow().strftime('%Y%m%d')
    confirmation_code = hmac.new(str(user.username), key.encode('utf-8'), hashlib.sha256).digest()
    confirmation_code = confirmation_code.encode('base-64').strip().replace('+', '')

    subject = 'Activate your blog account.'
    message = 'To activate your blog account click link: {0}?c={1}&u={2}'.format(activation_url,
                                                                                 confirmation_code,
                                                                                 user.id)
    send_mail(subject, message,  'from@example.com', [user.email])

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
    now = datetime.datetime.utcnow()
    delta = now - converted_date
    if delta > datetime.timedelta(minutes=5) or signature is None:
        raise WrongAuthorizeHeadersAPIError()

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist as e:
        raise UserDoesNotExistAPIError(e.message)

    access_token = user.get_session_auth_hash() + now.strftime('%Y%m%d')

    string_to_sign = datestamp + str(user_id)
    generated_signature = hmac.new(access_token, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    generated_signature = generated_signature.encode('base-64').strip()
    if generated_signature == signature:
        return user
    else:
        raise WrongAuthorizeHeadersAPIError()


# u - user id, c - activation code
def activate(u, c, email_activation_url, date=None):
    # argument date use only for testing
    if date is None:
        date = datetime.datetime.utcnow().strftime('%Y%m%d')

    mailed_code = c

    if mailed_code is None:
        raise WrongActivationCodeApiError('Missed user activation code')

    try:
        user = User.objects.get(id=u)
    except User.DoesNotExist as e:
        raise UserDoesNotExistAPIError(e.message)

    if user.is_active:
        return True

    key = email_activation_url + settings.SECRET_KEY + date
    confirmation_code = hmac.new(str(user.username), key.encode('utf-8'), hashlib.sha256).digest()
    confirmation_code = confirmation_code.encode('base-64').strip().replace('+', '')

    if confirmation_code == mailed_code:
        user.is_active = True
        user.save()
        return True
    else:
        subject = 'Activate your blog account.'
        message = 'To activate your blog account click link: {0}?c={1}&u={2}'.format(email_activation_url,
                                                                                     confirmation_code,
                                                                                     user.id)
        send_mail(subject, message, 'from@example.com', [user.email])
        raise WrongActivationCodeApiError('Wrong activation code')

