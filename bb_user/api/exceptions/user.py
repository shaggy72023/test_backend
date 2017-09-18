from utils.api.exceptions import APIError


class AuthAPIError(APIError):
    pass


class UsernameExistsAPIError(AuthAPIError):
    code = 'username_is_exists'


class WrongCredentialsAPIError(AuthAPIError):
    code = 'wrong_credentials'


class UserDoesNotExistAPIError(AuthAPIError):
    code = 'user_does_not_exist'


class WrongAuthorizeHeadersAPIError(AuthAPIError):
    code = 'wrong_authorize_headers'
