import datetime


def serialize(user):
    return {
        'user_id': user.id,
        'username': user.username
    }


def serialize_access_token(user):
    return {
        'user_id': user.id,
        'access_token': user.get_session_auth_hash() + datetime.datetime.utcnow().strftime('%Y%m%d')
    }
