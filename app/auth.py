from functools import wraps

from flask import current_app, request


UNAUTHORIZED_RESPONSE = {
    'message': 'Unauthorized'
}


def require_bearer_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return UNAUTHORIZED_RESPONSE, 401

        provided_token = auth_header.replace('Bearer ', '', 1).strip()
        expected_token = current_app.config['PREDEFINED_AUTH_TOKEN']
        if provided_token != expected_token:
            return UNAUTHORIZED_RESPONSE, 401

        return fn(*args, **kwargs)

    return wrapper
