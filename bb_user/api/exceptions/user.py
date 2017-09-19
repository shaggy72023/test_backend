from utils.api.exceptions import APIError


class AuthAPIError(APIError):
    pass


class FormValidationFailsApiError(AuthAPIError):
    code = 'form_validation_fails'


class WrongCredentialsAPIError(AuthAPIError):
    code = 'wrong_credentials'


class UserDoesNotExistAPIError(AuthAPIError):
    code = 'user_does_not_exist'


class WrongAuthorizeHeadersAPIError(AuthAPIError):
    code = 'wrong_authorize_headers'


class WrongActivationCodeApiError(AuthAPIError):
    code = 'wrong_activation_code'
